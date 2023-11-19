import requests, time, random
from requests_html import HTMLSession
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Max
from .models import ExchangeRates
from .serializers import ExchangeRatesSerializer


## crawling
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
# import matplotlib.pyplot as plt
from io import BytesIO
import base64


# Create your views here.
@api_view(['GET'])
def save_exchange_rates(request):
    api_key = 'VZuN8cgkfjO4hxiYFqEyk6B1RKaJdeZz'
    today = datetime.now()
    # 주말이면 이전 금요일
    if today.weekday() in [5, 6]:
        days_until_friday = (today.weekday() - 4) % 7
        last_friday = today - timedelta(days=days_until_friday)
        search_date = last_friday.strftime('%Y%m%d')
        
    else:
        search_date = today.strftime('%Y%m%d')

    # search_date = datetime.now().strftime('%Y%m%d')
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


@api_view(['GET'])
def crawling_news(request, keyword):
    if request.method == "GET":
        print('####', keyword)
        # keyword = request.GET.get('keyword')
        # keyword = 'USD'
        # url = f'https://www.google.com/search?q={keyword}&newwindow=1&tbm=nws&ei=TUmuY5LlINeghwOfw7egDQ&start=0&sa=N&ved=2ahUKEwjSv42woqD8AhVX0GEKHZ_hDdQQ8tMDegQIBBAE&biw=763&bih=819&dpr=2.2'

        # ChromeDriver 경로 설정
        driver = webdriver.Chrome()
        timesleep = random.randint(1, 10)
        # 구글 뉴스 페이지 열기
        driver.get(f'https://news.google.com/search?q={keyword}')
        time.sleep(timesleep)

        title_list = []
        link_list = []
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        h3_tag_list = soup.select('body h3')
        for i, tag in enumerate(h3_tag_list):
            if i >= 10:
                break
            title_list.append(tag.text)
            a_tag = tag.find('a')
            if a_tag:
                link_list.append(a_tag['href'])
        
        # print("Titles:", title_list)
        # print("Links:", link_list)

        # WebDriver 종료
        driver.quit()

        response_data = {
            'title_list': title_list,
            'link_list': link_list,
        }

        # JsonResponse를 사용하여 JSON 응답을 생성
        return JsonResponse(response_data)
    





    
        # # 뉴스 제목 추출
        # titles = driver.find_element(By.XPATH,"//a[@class='DY5T1d']")
        # for title in titles:
        #     print(title.text)
        #     print(title.get_attribute('href'))



        # driver = webdriver.Chrome()  # Chrome 드라이버 사용
        # driver.maximize_window()

        # # 나머지 코드
        # page = 1
        # title_list = []
        # content_list = []
        # link_list = []
        # timesleep = random.randint(1, 10)

        # for i in range(0, 20, 10):
        #     driver.get(url)

        #     # 일정 시간 동안 기다림 (1초 ~ 10초 사이의 랜덤한 시간)
        #     time.sleep(timesleep)

        #     print("*" * 10 + str(page) + "*" * 10)
        #     page += 1

        #     titles = driver.find_elements(By.CLASS_NAME, 'mCBkyc')
        #     for title in titles:
        #         title_list.append(title.text.replace(",", ""))

        #     contents = driver.find_elements(By.CLASS_NAME, 'GI74Re')
        #     for content in contents:
        #         content_list.append(content.text.replace(",", ""))

        #     links = driver.find_elements(By.CLASS_NAME, 'WlydOe')
        #     for link in links:
        #         link_list.append(link.get_attribute('href'))

        # # WebDriver 종료
        # driver.quit()

        # # 응답 데이터를 JSON 형식으로 구성
        # response_data = {
        #     'title': title_list,
        #     'content': content_list,
        #     'link': link_list,
        # }

        # # JsonResponse를 사용하여 JSON 응답을 생성
        # return JsonResponse(response_data)