from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import CommentSerializer, ArticleListSerializer, ArticleSerializer, ArticleBankCategorySerializer, ArticleProductCategorySerializer
from .models import Article, Comment, ArticleBankCategory, ArticleProductCategory
from products.models import SavingProducts, DepositProducts


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print('!!!')
        print(request.data)
        print(request.user)
        article_bank_category = ArticleBankCategory.objects.get(pk=request.data['article_bank_category'])
        article_product_category = ArticleProductCategory.objects.get(pk=request.data['article_product_category'])
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            serializer.save(user=request.user, article_bank_category=article_bank_category, article_product_category=article_product_category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET', 'POST'])
def product_category_list(request):
    if request.method == 'GET':
        products = get_list_or_404(ArticleProductCategory)
        serializer = ArticleProductCategorySerializer(products, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def bank_category_list(request):
    if request.method == 'GET':
        banks = get_list_or_404(ArticleBankCategory)
        serializer = ArticleBankCategorySerializer(banks, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        dep_banks = DepositProducts.objects.all().values('kor_co_nm')
        sav_banks = SavingProducts.objects.all().values('kor_co_nm')
        banks = ArticleBankCategory.objects.all()
        dep_banks = list(dep_banks)
        sav_banks = list(sav_banks)
        banks = list(banks)
        bank_list = dep_banks + sav_banks

        result = []
        for bank in bank_list:
            result.append(bank['kor_co_nm'])
        result = set(result)

        for bank in result:
            if bank not in banks:
                banks.append({'name': bank})
        
        serializer = ArticleBankCategorySerializer(data=banks, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'message': 'saved'})
        else:
            return Response({ 'message': 'not worked'})
    

@api_view(['GET', 'POST', 'DELETE'])
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
    

@api_view(['PUT', 'DELETE'])
def comment_control(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# @api_view(['GET'])
# def bank_list(request):
#     if request.method == 'GET':
#         dep_banks = DepositProducts.objects.all().only('kor_co_nm')
#         sav_banks = SavingProducts.objects.all().only('kor_co_nm')
#         print(dep_banks)
#         print(sav_banks)
#         return Response(dep_banks)
