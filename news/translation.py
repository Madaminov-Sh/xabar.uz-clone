from modeltranslation.translator import TranslationOptions, translator
from .models import Post, Category

# @register(Post)
class PostTranslationOption(TranslationOptions):
    fields = ('title', 'body',)

translator.register(Post, PostTranslationOption)

# @register(Category)
class CategoryTranslationOption(TranslationOptions):
    fields = ('title',)

translator.register(Category, CategoryTranslationOption)