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


# Create your views here.
@api_view(['GET'])
def save_exchange_rates(request):
    api_key = 'VZuN8cgkfjO4hxiYFqEyk6B1RKaJdeZz'
    search_date = datetime.now().strftime('%Y%m%d')
    url = f' https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&searchdate={search_date}&data=AP01'

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



@api_view(['GET', 'POST'])
def exchange(request):
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


