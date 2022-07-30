from django.db import models
from helpers.models import BaseModel
# Create your models here.
from ckeditor_uploader.fields import RichTextUploadingField
from common.models import User


class Category(BaseModel):
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=256, null=True, blank=True)
    icon = models.FileField(upload_to="category/", null=True, blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Option(BaseModel):
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=256, null=True, blank=True)
    category = models.ForeignKey(Category, related_name="options", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class OptionValue(BaseModel):
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=256, null=True, blank=True)
    option = models.ForeignKey(Option, related_name="options", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=256, null=True, blank=True)
    content = RichTextUploadingField()
    image = models.ImageField(
        upload_to="product_image", editable=False, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    in_stock = models.IntegerField(default=0)

    price = models.DecimalField(
        max_digits=19, decimal_places=2, verbose_name="Sotilish narxi")
    price_discount = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=True, verbose_name="Chegirmadagi narxi(ustiga chizilgan)")

    rate = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    saveds = models.ManyToManyField(User, related_name="saved_products")

    option_value = models.ManyToManyField(OptionValue, related_name="option_values")

    def set_image(self):
        main_image = ProductImage.objects.filter(
            product=self, is_main=True).first()
        self.image = main_image
        self.save()

    def __str__(self):
        return self.title


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_image/")
    is_main = models.BooleanField(default=False)


class Comment(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    content = models.TextField()

    def __str__(self):
        return self.content


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(blank=False)
    quantity = models.IntegerField(null=True)



