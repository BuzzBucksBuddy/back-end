import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Max
from .models import ExchangeRates
from .serializers import ExchangeRatesSerializer


# ## crawling
# from bs4 import BeautifulSoup
# from selenium import webdriver
# import matplotlib.pyplot as plt
# from io import BytesIO
# import base64


# Create your views here.
@api_view(['GET'])
def save_exchange_rates(request):
    api_key = 'VZuN8cgkfjO4hxiYFqEyk6B1RKaJdeZz'
    search_date = datetime.now().strftime('%Y%m%d')
    url = f' https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&searchdate={search_date}&data=AP01'
    # url = f' https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&searchdate=20230215&data=AP01'
    

    ## 테이블 리셋
    curr_data = ExchangeRates.objects.all()
    curr_data.delete()

    # api 응답 데이터로 테이블 저장 
    response = requests.get(url).json()
    for li in response:
        save_data = {
            'result': li.get('result'),
            'cur_unit': li.get('cur_unit'),
            'ttb': li.get('ttb'),
            'tts': li.get('tts'),
            'deal_bas_r': li.get('deal_bas_r'),
            'bkpr': li.get('bkpr'),
            'yy_efee_r': li.get('yy_efee_r'),
            'ten_dd_efee_r': li.get('ten_dd_efee_r'),
            'kftc_bkpr': li.get('kftc_bkpr'),
            'kftc_deal_bas_r': li.get('kftc_deal_bas_r'),
            'cur_nm': li.get('cur_nm'),
        }
        serializer = ExchangeRatesSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    
    return JsonResponse({ 'message': 'okay'})


@api_view(['GET'])
def find_country_info(request, country, category):
    if request.method == "GET":
        country_info = ExchangeRates.objects.get(cur_unit=country)
        print(country_info)
        # exchange_rate = country_info.values(category)
        # print('333',exchange_rate)

        unit = country_info.cur_nm.split()[-1]
        
        if category == 'ttb':
            exchange_rate = country_info.ttb
        elif category == 'tts':
            exchange_rate = country_info.tts
        elif category == 'deal_bas_r':
            exchange_rate = country_info.ttb
        

        # exchage_rate = country_info.i
        # print(exchage_rate)
        # serializer = ExchangeRatesSerializer(exchange_rate)

    # elif request.method == "POST":
    #     serializer = ExchangeRatesSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({ 'message': '이미 있는 데이터이거나, 데이터가 잘못 입력되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'rate': exchange_rate, 'unit': unit})



@api_view(['GET', 'POST'])
def exchange_all(request):
    if request.method == "GET":
        exchange_rates = ExchangeRates.objects.all()
        serializer = ExchangeRatesSerializer(exchange_rates, many=True)

    # elif request.method == "POST":
    #     serializer = ExchangeRatesSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({ 'message': '이미 있는 데이터이거나, 데이터가 잘못 입력되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.data)
    # return JsonResponse(response, safe=False)  # safe=False를 추가함으로써, 딕셔너리 이외의 객체도 직렬화할 수 있음


