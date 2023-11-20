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
from .serializers import CustomRegisterSerializer, FavoriteSerializer


# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    # user = User.objects.get(pk=request.user.id)   ## 직접참조 말고 변경
    if request.method == 'GET':
        serializer = CustomRegisterSerializer(request.user)   
        return Response(serializer.data)
    
    else:
        return Response({'detail': '인증이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
    # elif request.method == 'POST':
    #     serializer = CustomRegisterSerializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def favorite_category(request):
    if request.method == "GET":
        favorites = Favorite.objects.all()
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = FavoriteSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
