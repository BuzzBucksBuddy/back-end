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
        print(request.user.id)
        user = get_object_or_404(get_user_model(), pk=request.user.id)
        print(type(user))
        serializer = UpdateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            print(request.user)
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

@permission_classes([IsAuthenticated])
def users_favorite(request):
    # me = get_object_or_404(get_user_model(), pk=request.user.id).id
    me = Favorite.user_set.get()
    # my = CustomRegisterSerializer(request.user)['favorite']
    print(me, '######')
    for myfavorite in my:
        print(myfavorite)
    # me = get_object_or_404(get_user_model(), pk=request.user.id)
    my_favorites = Favorite.user_set.filter()
    print(my_favorites)
    # favorite = random.sample(my_favorites, 1)
    # print(favorite,'000')
    # users = get_list_or_404(get_user_model()).filter(favorite_id)
    # for user in users:
    #     if favorite in user.favorite:
    #         pass

    return Response({'message': 'favorite 추천 ok?'})

