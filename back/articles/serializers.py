from rest_framework import serializers
from .models import Article, Comment, ArticleBankCategory, ArticleProductCategory
from django.contrib.auth import get_user_model


class ArticleListSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('username',)

    class ArticleProductCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = ArticleProductCategory
            fields = ('name',)
    
    class ArticleBankCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = ArticleBankCategory
            fields = ('name',)
    
    user = UserSerializer(read_only=True)
    article_product_category = ArticleProductCategorySerializer(read_only=True)
    article_bank_category = ArticleBankCategorySerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('username',)
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article', 'like_users',)


class ArticleSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'username',)

    class ArticleProductCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = ArticleProductCategory
            fields = ('id', 'name',)
    
    class ArticleBankCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = ArticleBankCategory
            fields = ('id', 'name',)
    
    user = UserSerializer(read_only=True)
    article_product_category = ArticleProductCategorySerializer(read_only=True)
    article_bank_category = ArticleBankCategorySerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('like_users', 'user',)


class ArticleBankCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleBankCategory
        fields = '__all__'


class ArticleProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleProductCategory
        fields = '__all__'
