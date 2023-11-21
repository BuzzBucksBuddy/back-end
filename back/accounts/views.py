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
@permission_classes([IsAuthenticated])
def users_age(request, age):
    set_range = 5
    min_age = 1
    if (age - set_range) > 1:
        min_age = age - set_range
    users = get_user_model().objects.filter(age__range=[min_age, age + set_range])

    all_user_financial_products_dep = DepositProducts.objects.filter(dep_users__in=users)
    financial_products_dep_counts = all_user_financial_products_dep.values('id').annotate(count=Count('id'))
    sorted_financial_products_dep = financial_products_dep_counts.order_by('-count')
    most_financial_products_dep = list(sorted_financial_products_dep[:5])

    all_user_financial_products_sav = SavingProducts.objects.filter(sav_users__in=users)
    financial_products_sav_counts = all_user_financial_products_sav.values('id').annotate(count=Count('id'))
    sorted_financial_products_sav = financial_products_sav_counts.order_by('-count')
    most_financial_products_sav = list(sorted_financial_products_sav[:5])

    response_data = {
        'most_financial_products_dep': most_financial_products_dep,
        'most_financial_products_sav': most_financial_products_sav,
    }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_money(request, money):
    set_range = 10000000
    min_money = 0
    if (money - set_range) > 0:
        min_money = money - set_range
    users = get_user_model().objects.filter(money__range=[min_money, money + set_range])

    all_user_financial_products_dep = DepositProducts.objects.filter(dep_users__in=users)
    financial_products_dep_counts = all_user_financial_products_dep.values('id').annotate(count=Count('id'))
    sorted_financial_products_dep = financial_products_dep_counts.order_by('-count')
    most_financial_products_dep = list(sorted_financial_products_dep[:5])

    all_user_financial_products_sav = SavingProducts.objects.filter(sav_users__in=users)
    financial_products_sav_counts = all_user_financial_products_sav.values('id').annotate(count=Count('id'))
    sorted_financial_products_sav = financial_products_sav_counts.order_by('-count')
    most_financial_products_sav = list(sorted_financial_products_sav[:5])

    response_data = {
        'most_financial_products_dep': most_financial_products_dep,
        'most_financial_products_sav': most_financial_products_sav,
    }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_salary(request, salary):
    set_range = 5000000
    min_salary = 0
    if (salary - set_range) > 0:
        min_salary = salary-set_range
    users = get_user_model().objects.filter(salary__range=[min_salary, salary + set_range])

    all_user_financial_products_dep = DepositProducts.objects.filter(dep_users__in=users)
    financial_products_dep_counts = all_user_financial_products_dep.values('id').annotate(count=Count('id'))
    sorted_financial_products_dep = financial_products_dep_counts.order_by('-count')
    most_financial_products_dep = list(sorted_financial_products_dep[:5])

    all_user_financial_products_sav = SavingProducts.objects.filter(sav_users__in=users)
    financial_products_sav_counts = all_user_financial_products_sav.values('id').annotate(count=Count('id'))
    sorted_financial_products_sav = financial_products_sav_counts.order_by('-count')
    most_financial_products_sav = list(sorted_financial_products_sav[:5])

    response_data = {
        'most_financial_products_dep': most_financial_products_dep,
        'most_financial_products_sav': most_financial_products_sav,
    }
    return Response(response_data)


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


@api_view(['GET'])
def dep_users(reqest, fin_prdt_cd):
    product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    users = get_user_model().objects.filter(financial_products_dep__pk=product.id)
    users_id = []
    for user in users:
        users_id.append(user.id)

    response_data = {
        'users': users_id
    }
    return Response(response_data)


@api_view(['GET'])
def sav_users(reqest, fin_prdt_cd):
    product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    users = get_user_model().objects.filter(financial_products_sav__pk=product.id)
    users_id = []
    for user in users:
        users_id.append(user.id)

    response_data = {
        'users': users_id
    }
    return Response(response_data)
