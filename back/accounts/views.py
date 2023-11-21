from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import User, CustomAccountAdapter, Favorite
from products.models import DepositProducts, SavingProducts
from .serializers import CustomRegisterSerializer, FavoriteSerializer, UpdateUserSerializer

import random
from django.db.models import Count

# Create your views here.

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    # user = User.objects.get(pk=request.user.id)   ## 직접참조 말고 변경
    if request.method == 'GET':
        serializer = CustomRegisterSerializer(request.user)   
        return Response(serializer.data)
    
    # else:
    #     return Response({'detail': '인증이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'PUT':
        user = get_object_or_404(get_user_model(), pk=request.user.id)
        serializer = UpdateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_category(request):
    if request.method == "GET":
        favorites = Favorite.objects.all()
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_select(request, favorite_pk):
    favorite = Favorite.objects.get(pk=favorite_pk)
    if request.method == "POST":
        if request.user in favorite.user_set.all():
            favorite.user_set.remove(request.user)
        else:
            favorite.user_set.add(request.user)
        return Response({'message':'This is my favorite thing.'})
        # serializer = CustomRegisterSerializer(request.user, data=request.data, partial=True)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save(user=request.user)
            
            # favorites = []
            # for favorite_id in request.data.get('favorites'):
            #     try:
            #         favorite = Favorite.objects.get(id=favorite_id)
            #         favorites.append(favorite)
            #     except:
            #         raise NotFound()
            # User.favorites.set(favorites)
            # return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])

def users_age(request):
    # user = get_object_or_404(get_user_model(), pk=request.user.id)
    age = 10
    users = get_list_or_404(get_user_model())
    filtered_users = []
    dep_products = []
    sav_products = []
    for user in users:
        if user.age in range(age - 2, age + 3):
            filtered_users.append(user)
    for user in filtered_users:
        print(user)
        dep_products.append(user.financial_products_dep)
        sav_products.append(user.financial_products_sav)
    print(type(dep_products))
    return Response({'message': 'ok?'})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_favorite(request, favorite_pk):
    users_with_favorite = get_user_model().objects.filter(favorite__pk=favorite_pk)  # 해당 favorite가진 사람들
    # print(users_with_favorite)
    
    ## 예금 랭킹
    all_user_financial_products_dep = DepositProducts.objects.filter(dep_users__in=users_with_favorite)  # 이사람들이 사용한 상품 전체
    financial_products_dep_counts = all_user_financial_products_dep.values('id').annotate(count=Count('id')) # 상품 전체에서 id들을 구하고, id 필드에 대한 집계 함수를 추가
    sorted_financial_products_dep = financial_products_dep_counts.order_by('-count') # count 필드기준으로ㄴ 내림차순 정렬
    most_financial_products_dep = list(sorted_financial_products_dep[:5])
    
    ## 적금 랭킹
    all_user_financial_products_sav = SavingProducts.objects.filter(sav_users__in=users_with_favorite)
    financial_products_sav_counts = all_user_financial_products_sav.values('id').annotate(count=Count('id'))
    sorted_financial_products_sav = financial_products_sav_counts.order_by('-count')
    most_financial_products_sav = list(sorted_financial_products_sav[:5])
    
    response_data = {
        'most_financial_products_dep': most_financial_products_dep,
        'most_financial_products_sav': most_financial_products_sav,
    }

    return Response(response_data)
    # return Response({'message': f'financial_products_dep 랭킹: {most_common_financial_products_dep}'})
    # print(users_with_favorite)
    # favorite = Favorite.user_set.filter(pk=favorite_pk).exists()
    # print(favorite)
    # me = get_object_or_404(get_user_model(), pk=request.user.id).id
    # my = CustomRegisterSerializer(request.user)['favorite']
    # me = get_object_or_404(get_user_model(), pk=request.user.id)
    # for user in users_with_favorite:
   
   
    # favorite_counts = Favorite.objects.filter(user_set__in=users_with_favorite).values('id').annotate(count=Count('id'))    
    # print(favorite_counts)
    # most_favorite = favorite_counts.order_by('-count').first()
    # # most_favorite = favorite_counts.order_by('-count')
    # print('###',most_favorite)
    # # favorite = random.sample(my_favorites, 1)
    # # print(favorite,'000')
    # # users = get_list_or_404(get_user_model()).filter(favorite_id)
    # # for user in users:
    # #     if favorite in user.favorite:
    # #         pass

    # return Response({'message': 'favorite 추천 ok?'})

