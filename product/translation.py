from modeltranslation.translator import translator, TranslationOptions
from .models import Product


class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


translator.register(Product, ProductTranslationOptions)
