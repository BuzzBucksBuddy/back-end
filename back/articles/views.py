from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import CommentSerializer, ArticleListSerializer, ArticleSerializer, ArticleBankCategorySerializer, ArticleProductCategorySerializer
from .models import Article, Comment, ArticleBankCategory, ArticleProductCategory
from products.models import SavingProducts, DepositProducts


# 게시글 CREATE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_create(request):
    if request.method == 'POST':
        article_bank_category = ArticleBankCategory.objects.get(pk=request.data['article_bank_category'])
        article_product_category = ArticleProductCategory.objects.get(pk=request.data['article_product_category'])
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            serializer.save(user=request.user, article_bank_category=article_bank_category, article_product_category=article_product_category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 게시글 READ ALL
@api_view(['GET'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all().order_by("-updated_at")
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)


# 게시글 READ
@api_view(['GET'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


# 게시글 categorized READ
@api_view(['GET'])
def article_categorize(request, product_pk, bank_pk):
    if request.method == 'GET':
        if (product_pk == 0) and (bank_pk == 0):
            articles = Article.objects.all().order_by("-updated_at")
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data)
            
        elif product_pk != 0 and bank_pk == 0:
            articles = Article.objects.filter(article_product_category=product_pk).order_by("-updated_at")
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data)
        
        elif product_pk == 0 and bank_pk != 0:
            articles = Article.objects.filter(article_bank_category=bank_pk).order_by("-updated_at")
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data)

        else:
            print('!!!')
            articles = Article.objects.filter(article_bank_category=bank_pk, article_product_category=product_pk).order_by("-updated_at")
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data)


@api_view(['GET'])
def article_search(request, field, input):
    if request.method == 'GET':
        if field == 'title':
            articles = Article.objects.filter(title__contains=input).order_by("-updated_at")
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data)
        
        elif field == 'content':
            articles = Article.objects.filter(content__contains=input).order_by("-updated_at")
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data)
        
        else:
            by_title = Article.objects.filter(title__contains=input)
            by_content = Article.objects.filter(content__contains=input)
            articles = by_title | by_content
            articles = articles.order_by("-updated_at")
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data)


# 게시글 DELETE, UPDATE
@api_view(['DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def article_control(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    
    if request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


# 카테고리(예금, 적금 등등) READ
@api_view(['GET', 'POST'])
def product_category_list(request):
    if request.method == 'GET':
        products = get_list_or_404(ArticleProductCategory)
        serializer = ArticleProductCategorySerializer(products, many=True)
        return Response(serializer.data)


# 카테고리(은행) READ & (CREATE, UPDATE)
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


# 코멘트 READ
@api_view(['GET'])
def comment_list(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        comments = Comment.objects.filter(article=article)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

# 코멘트 CREATE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 코멘트 UPDATE, DELETE
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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


# 게시글 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_like(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        if request.user in article.like_users.all():
            article.like_users.remove(request.user)
        else:
            article.like_users.add(request.user)
        return Response({ 'message': 'like_you?'})


# 코멘트 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_like(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        if request.user in comment.like_users.all():
            comment.like_users.remove(request.user)
        else:
            comment.like_users.add(request.user)
        return Response({ 'message': 'like_you?'})
