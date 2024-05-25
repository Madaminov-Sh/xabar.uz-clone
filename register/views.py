from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect

from register.forms import LoginForm, NewUserForm, EditUserForm, EditProfileForm
from register.models import Profile


def log_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, 
                                username = data['username'],
                                password = data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('news:index_page')
            else:
                return HttpResponse('bunday user mavjud emas')

    context = {'form':form}
    return render(request,'registration/login.html', context)


def signup(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.filter(user = new_user)
            return redirect('register:login')

    return render(request,'registration/signup.html', {'form':form,}) 


@login_required()
# @user_passes_test
def userprofile(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    return render(request, 'profile/user_profile.html', {'user':user, 'profile':profile})


        # userning (dashbord) malumotlarini tahrirlash 
@login_required()
def edit_user(request):
    if request.method == 'POST':
        edit_user_form = EditUserForm(instance=request.user, data=request.POST)
        edit_profile_form = EditProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if edit_user_form.is_valid() and edit_profile_form.is_valid():
            edit_user_form.save()
            edit_profile_form.save()
            return redirect('register:profile')

    else:
        edit_user_form = EditUserForm(instance=request.user)
        edit_profile_form = EditProfileForm(instance=request.user.profile)

    return render(request, 'profile/edit_user_profile.html', {'user_form':edit_user_form, 'profile_form':edit_profile_form})