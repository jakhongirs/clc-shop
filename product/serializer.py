from rest_framework import serializers
from .models import Product, Category, Comment, ProductImage
from common.models import User
from common.serializer import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    comments = CommentSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ('category', 'images', 'comments',)
