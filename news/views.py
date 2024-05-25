from django.db.models import Q
from django.shortcuts import get_object_or_404
from common.custom_permissions import OnlyLoggedSuperuserMixin
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy

from hitcount.views import HitCountMixin
from hitcount.utils import get_hitcount_model

from news.models import Post, Category
from register.models import User
from news.forms import ContactModelForm, CommentForm


class IndexView(generic.ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['mine_slide_posts'] = Post.published.all().order_by('-publish_time')[:4]
        return context
        
'''==============================================================='''

# class PostDetailView(generic.DetailView):
#     model = Post
#     template_name = 'detail.html'
#     context_object_name = 'post'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         post.view_count = post.view_count +1
#         post.comment = post.comments.filter(comment_post=post)
#         post.save() # result: None
#         form = CommentForm()
#         new_comment = None
#         if self.request.method == 'POST':
#             form = CommentForm(data=self.request.POST)
#             if form.is_valid():
#                 new_comment = form.save(commit=False)
#                 new_comment.comment_post_id = post.id
#                 new_comment.comment_user_id = self.request.user.id
#                 new_comment.save()
#                 # form = CommentForm()

#         context['post_count'] = post.view_count # ko'rishlar sonini xisoblash
#         context['post_comment'] = post.comment # kamentlarni postlarga filterlash
#         context['new_comment'] = new_comment # formdan kelgan yangi kamentlar
#         context['form'] = form # kament form
#         return context
"""===================================================================================="""
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = CommentForm(request.POST)
    #     comment = None
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.comment_post = self.object
    #         comment.comment_user = request.user
    #         comment.save()
    #         print(f'bu com save: {com_save}')
    #         return render(request, 'detail.html', {'form':form, 'comment':comment})

    #     return redirect('news:post_detail_page', slug=self.object.slug)

"""sorov yuborilmayabdi, frontend form ichini ko'rish kerak"""


def detailview(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.published)
    post_comment = post.comments.filter(comment_post=post)

    # hit count
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(post)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hitcount_response = HitCountMixin.hit_count(request, hit_count)

    if hitcount_response.hit_counted:
        hits += 1
        hitcontext['hit_counted'] = hitcount_response.hit_counted
        hitcontext['hit_counted'] = hitcount_response.hit_counted
        hitcontext['total_hits'] = hits

    post.save()
    form = CommentForm()
    new_comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.comment_post_id = post.id
            new_comment.comment_user_id = request.user.id
            new_comment.save()
            form = CommentForm()

    context = {
        'form':form,
        'post_comment':post_comment,    
        'post':post,
        'new_comment':new_comment,
    }
    return render(request, 'detail.html', context)


class PostCreateView(OnlyLoggedSuperuserMixin, generic.CreateView):
    model = Post
    template_name = 'crud/post_create.html'
    fields = ('title', 'title_uz', 'title_en', 'title_ru',
              'slug', 'body', 'body_uz', 'body_en',
              'body_ru', 'image', 'category', 'status')


class PostUpdateView(OnlyLoggedSuperuserMixin, generic.UpdateView):
    model = Post
    template_name = 'crud/post_update.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status',)
    

class PostDeleteView(OnlyLoggedSuperuserMixin, generic.DeleteView):
    model = Post
    template_name = 'crud/post_delete.html'
    success_url = reverse_lazy('news:index_page')


class ContactView(OnlyLoggedSuperuserMixin, generic.TemplateView):
    template_name = 'contact.html'

    def post(self, request, *args, **kwargs):
        form = ContactModelForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('news:indexpage')
        return render(request, 'contact.html', {'form':form})


class AdminPageView(OnlyLoggedSuperuserMixin, generic.ListView):
    queryset = User.objects.filter(is_superuser=True)
    template_name = 'admins_page.html'
    context_object_name = 'admins'


class SearchResultView(generic.ListView):
    model = Post
    template_name = 'details/search.html'
    context_object_name = 'searches'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.published.filter(Q(title__icontains=query) or Q(body__icontains=query))
