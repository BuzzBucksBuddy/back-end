from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

# from .serializers import 
# from .models import 
# from products.models import 


# Create your views here.
# @api_view(['GET', 'POST'])
# def my_profile(request, nickname):
