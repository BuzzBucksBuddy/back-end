from rest_framework import serializers
from .models import Article, Comment, ArticleBankCategory, ArticleProductCategory


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ArticleBankCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleBankCategory
        fields = '__all__'


class ArticleProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleProductCategory
        fields = '__all__'
