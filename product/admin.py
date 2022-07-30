from django.contrib import admin

# Register your models here.
from django.apps import apps

from django.contrib import admin
from .models import Product
from modeltranslation.admin import TranslationAdmin


class ProductAdmin(TranslationAdmin):
    pass


admin.site.register(Product, ProductAdmin)

models = apps.get_models()
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
