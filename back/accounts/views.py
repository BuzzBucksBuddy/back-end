from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings
from django.contrib.auth import get_user_model

from .serializers import CustomRegisterSerializer
from .models import User, CustomAccountAdapter
from products.models import DepositProducts, SavingProducts


# Create your views here.
@api_view(['GET', 'POST'])
def my_profile(request, nickname):
    user = User.objects.get(nickname=nickname)   ## 직접참조 말고 변경
    if request.method == 'GET':
        serializer = CustomRegisterSerializer(user)   
        return Response(serializer.data)
    
    else:
        return Response({'detail': '인증이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
    # elif request.method == 'POST':
    #     serializer = CustomRegisterSerializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
