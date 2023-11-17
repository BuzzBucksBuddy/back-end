from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import CommentSerializer, ArticleListSerializer, ArticleSerializer, ArticleBankCategorySerializer, ArticleProductCategorySerializer
from .models import Article, Comment, ArticleBankCategory, ArticleProductCategory


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print('!!!')
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


@api_view(['GET'])
def product_category_list(request):
    if request.method == 'GET':
        products = get_list_or_404(ArticleProductCategory)
        serializer = ArticleProductCategorySerializer(products, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def bank_category_list(request):
    if request.method == 'GET':
        banks = get_list_or_404(ArticleBankCategory)
        serializer = ArticleBankCategorySerializer(banks, many=True)
        return Response(serializer.data)
    

@api_view(['GET', 'POST'])
def comment_list(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        comments = Comment.objects.filter(article=article)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
