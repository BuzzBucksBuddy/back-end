from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import DepositProducts, SavingProducts, DepositOptions, SavingOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializer, SavingOptionsSerializer
import requests


# 상품 정보 전체 저장
@api_view(['GET'])
def products_data(request):
    API_KEY = '2d7916000e6e7a639cab7d9f3fa858be'
    url_dep = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
    url_sav = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

    response_dep = requests.get(url_dep).json()

    for li in response_dep.get('result').get('baseList'):
        try:
            DepositProducts.objects.get(fin_prdt_cd = li.get('fin_prdt_cd'))
        except:
            save_data = {
                'fin_prdt_cd': li.get('fin_prdt_cd'),
                'dcls_month': li.get('dcls_month'),
                'fin_co_no': li.get('fin_co_no'),
                'kor_co_nm': li.get('kor_co_nm'),
                'fin_prdt_nm': li.get('fin_prdt_nm'),
                'etc_note': li.get('etc_note'),
                'join_deny': li.get('join_deny'),
                'join_member': li.get('join_member'),
                'join_way': li.get('join_way'),
                'spcl_cnd': li.get('spcl_cnd'),
                'max_limit': li.get('max_limit'),
                'mtrt_int': li.get('mtrt_int'),
            }
            serializer = DepositProductsSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
    
    for li in response_dep.get('result').get('optionList'):
        save_data = {
            'fin_prdt_cd': li.get('fin_prdt_cd'),
            'intr_rate_type': li.get('intr_rate_type'),
            'intr_rate_type_nm': li.get('intr_rate_type_nm'),
            'intr_rate': li.get('intr_rate'),
            'intr_rate2': li.get('intr_rate2'),
            'save_trm': li.get('save_trm'),
        }
        
        serializer = DepositOptionsSerializer(data=save_data)
        product = DepositProducts.objects.get(fin_prdt_cd = save_data['fin_prdt_cd'])
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product)
    
    response_sav = requests.get(url_sav).json()

    for li in response_sav.get('result').get('baseList'):
        try:
            SavingProducts.objects.get(fin_prdt_cd = li.get('fin_prdt_cd'))
        except:
            save_data = {
                'fin_prdt_cd': li.get('fin_prdt_cd'),
                'dcls_month': li.get('dcls_month'),
                'fin_co_no': li.get('fin_co_no'),
                'kor_co_nm': li.get('kor_co_nm'),
                'fin_prdt_nm': li.get('fin_prdt_nm'),
                'etc_note': li.get('etc_note'),
                'join_deny': li.get('join_deny'),
                'join_member': li.get('join_member'),
                'join_way': li.get('join_way'),
                'spcl_cnd': li.get('spcl_cnd'),
                'max_limit': li.get('max_limit'),
                'mtrt_int': li.get('mtrt_int'),
            }
            serializer = SavingProductsSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
    
    for li in response_sav.get('result').get('optionList'):
        save_data = {
            'fin_prdt_cd': li.get('fin_prdt_cd'),
            'intr_rate_type': li.get('intr_rate_type'),
            'intr_rate_type_nm': li.get('intr_rate_type_nm'),
            'intr_rate': li.get('intr_rate'),
            'intr_rate2': li.get('intr_rate2'),
            'rsrv_type': li.get('rsrv_type'),
            'rsrv_type_nm': li.get('rsrv_type_nm'),
            'save_trm': li.get('save_trm'),
        }
        
        serializer = SavingOptionsSerializer(data=save_data)
        product = SavingProducts.objects.get(fin_prdt_cd = save_data['fin_prdt_cd'])
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product)
    
    return JsonResponse({ 'message' : 'Okay!' })


# 예금 상품 전체 조회
@api_view(['GET'])
def deposit_list(request):
    products = DepositProducts.objects.all()
    serializer = DepositProductsSerializer(products, many=True)
    return Response(serializer.data)


# 적금 상품 전체 조회
@api_view(['GET'])
def saving_list(request):
    products = SavingProducts.objects.all()
    serializer = SavingProductsSerializer(products, many=True)
    return Response(serializer.data)


# 예금 상품 단일 조회
@api_view(['GET'])
def deposit_product(request, fin_prdt_cd):
    product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositProductsSerializer(product)
    return Response(serializer.data)


# 적금 상품 단일 조회
@api_view(['GET'])
def saving_product(request, fin_prdt_cd):
    product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    serializer = SavingProductsSerializer(product)
    return Response(serializer.data)


# 예금 상품별 옵션 조회
@api_view(['GET'])
def deposit_options(request, fin_prdt_cd):
    product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    options = product.dep_option.all()
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)


# 적금 상품별 옵션 조회
@api_view(['GET'])
def saving_options(request, fin_prdt_cd):
    product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    options = product.sav_option.all()
    serializer = SavingOptionsSerializer(options, many=True)
    return Response(serializer.data)