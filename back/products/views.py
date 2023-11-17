from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .serializers import DepositProductsSerializer, DepositOptionsSerializer
from django.http import JsonResponse
from .models import DepositOptions, DepositProducts
from rest_framework import status


@api_view(['GET'])
def save_data(request):
    API_KEY = '2d7916000e6e7a639cab7d9f3fa858be'
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

    response = requests.get(url).json()

    for li in response.get('result').get('baseList'):
        try:
            DepositProducts.objects.get(fin_prdt_cd = li.get('fin_prdt_cd'))
        except:
            save_data = {
                'fin_prdt_cd': li.get('fin_prdt_cd'),
                'kor_co_nm': li.get('kor_co_nm'),
                'fin_prdt_nm': li.get('fin_prdt_nm'),
                'etc_note': li.get('etc_note'),
                'join_deny': li.get('join_deny'),
                'join_member': li.get('join_member'),
                'join_way': li.get('join_way'),
                'spcl_cnd': li.get('spcl_cnd')
            }
            serializer = DepositProductsSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
    
    for li in response.get('result').get('optionList'):
        save_data = {
            'fin_prdt_cd': li.get('fin_prdt_cd'),
            'intr_rate_type_nm': li.get('intr_rate_type_nm'),
            'intr_rate': li.get('intr_rate'),
            'intr_rate2': li.get('intr_rate2'),
            'save_trm': li.get('save_trm'),
        }
        
        serializer = DepositOptionsSerializer(data=save_data)
        product = DepositProducts.objects.get(fin_prdt_cd = save_data['fin_prdt_cd'])
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product)
    
    return JsonResponse({ 'message': 'okay'})


@api_view(['GET'])
def product_list(request):
    products = DepositProducts.objects.all()
    serializer = DepositProductsSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_options(request, fin_prdt_cd):
    product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    options = product.option.all()
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)