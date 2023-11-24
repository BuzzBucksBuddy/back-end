from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse, Http404
from .models import DepositProducts, SavingProducts, DepositOptions, SavingOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializer, SavingOptionsSerializer, OneDepOptSerializer, OneSavOptSerializer
import requests
from random import shuffle
from django.db.models import F

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


# 상품 정보 전체 저장
@api_view(['GET'])
def products_data(request):
    API_KEY = '2d7916000e6e7a639cab7d9f3fa858be'
    url_dep = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
    url_sav = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

    ## 테이블 리셋
    # curr_data_dep = DepositProducts.objects.all()
    # curr_data_sav = SavingProducts.objects.all()
    # curr_data_dep_op = DepositOptions.objects.all()
    # curr_data_sav_op = SavingOptions.objects.all()
    # curr_data_dep.delete()
    # curr_data_sav.delete()
    # curr_data_dep_op.delete()
    # curr_data_sav_op.delete()


    # 예금 상품/옵션 데이터 가져오기
    response_dep = requests.get(url_dep).json()

    dep_products_count = 0  # 예금 상품 개수 초기화
    
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
            dep_products_count += 1  # 예금 상품이 저장되면 개수 증가
    

    for li in response_dep.get('result').get('optionList'):
        exist = DepositOptions.objects.filter(fin_prdt_cd__contains=li.get('fin_prdt_cd')) & DepositOptions.objects.filter(save_trm__contains=li.get('save_trm'))
        if len(exist) == 0:
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
            

        
    # 적금 상품/옵션 데이터 가져오기
    response_sav = requests.get(url_sav).json()

    sav_products_count = 0  # 적금 상품 개수 초기화
    

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
            sav_products_count += 1  # 적금 상품이 저장되면 개수 증가
    
    for li in response_sav.get('result').get('optionList'):
        exist = SavingOptions.objects.filter(fin_prdt_cd__contains=li.get('fin_prdt_cd')) & SavingOptions.objects.filter(save_trm__contains=li.get('save_trm')) & SavingOptions.objects.filter(rsrv_type_nm__contains=li.get('rsrv_type_nm'))
        if len(exist) == 0:
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
            
    

    response_data = {
        'message': 'Okay!',
        'deposit_products_count': dep_products_count,
        'saving_products_count': sav_products_count,
    }

    return JsonResponse(response_data)


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


# 예금 상품 은행 별 조회
@api_view(['GET'])
def deposit_filtered(request, kor_co_nm):
    if request.method == 'GET':
        if kor_co_nm == '선택 안함':
            products = DepositProducts.objects.all()
            serializer = DepositProductsSerializer(products, many=True)
            return Response(serializer.data)
        else:
            products = DepositProducts.objects.filter(kor_co_nm__contains=kor_co_nm)
            serializer = DepositProductsSerializer(products, many=True)
            return Response(serializer.data)


# 적금 상품 은행 별 조회
@api_view(['GET'])
def saving_filtered(request, kor_co_nm):
    if request.method == 'GET':
        if kor_co_nm == '선택 안함':
            products = SavingProducts.objects.all()
            serializer = SavingProductsSerializer(products, many=True)
            return Response(serializer.data)
        else:
            products = SavingProducts.objects.filter(kor_co_nm__contains=kor_co_nm)
            serializer = SavingProductsSerializer(products, many=True)
            return Response(serializer.data)


# 예금 옵션 카테고라이즈
@api_view(['GET'])
def deposit_categorize(request, fin_prdt_cd, save_trm):
    if request.method == 'GET':
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        # 모두 가져오기
        if save_trm == 0:
            options = product.dep_option.all()
            serializer = DepositOptionsSerializer(options, many=True)
            return Response(serializer.data)
        # 저축 기간 필터링
        else:
            options = product.dep_option.filter(save_trm=save_trm)
            serializer = DepositOptionsSerializer(options, many=True)
            return Response(serializer.data)


# 적금 옵션 카테고라이즈
@api_view(['GET'])
def saving_categorize(request, fin_prdt_cd, save_trm, rsrv_type_nm):
    if request.method == 'GET':
        product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        # 모두 가져오기
        if rsrv_type_nm == '선택 안함':
            # 모두 가져오기
            if save_trm == 0:
                options = product.sav_option.all()
                serializer = SavingOptionsSerializer(options, many=True)
                return Response(serializer.data)
            # 저축 기간 필터링
            else:
                options = product.sav_option.filter(save_trm=save_trm)
                serializer = SavingOptionsSerializer(options, many=True)
                return Response(serializer.data)
        # 적립 유형 필터링
        else:
            # 모두 가져오기
            if save_trm == 0:
                options = product.sav_option.filter(rsrv_type_nm=rsrv_type_nm)
                serializer = SavingOptionsSerializer(options, many=True)
                return Response(serializer.data)
            # 저축 기간 필터링
            else:
                options = product.sav_option.filter(rsrv_type_nm=rsrv_type_nm, save_trm=save_trm)
                serializer = SavingOptionsSerializer(options, many=True)
                return Response(serializer.data)


# 예금 상품 가입하기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def become_my_dep_option(request, option_pk):
    option = DepositOptions.objects.get(id=option_pk)
    if request.method == 'POST':
        if request.user in option.dep_users.all():
            option.dep_users.remove(request.user)
        else:
            option.dep_users.add(request.user)
        return Response({ 'message': 'okay!'})


# 적금 상품 가입하기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def become_my_sav_option(request, option_pk):
    option = SavingOptions.objects.get(id=option_pk)
    if request.method == 'POST':
        if request.user in option.sav_users.all():
            option.sav_users.remove(request.user)
        else:
            option.sav_users.add(request.user)
        return Response({ 'message': 'okay!'})


# 상품이름으로 상품 찾기
@api_view(['GET'])
def find_product(request, pdt_name):
    product_dep = DepositProducts.objects.filter(fin_prdt_nm=pdt_name).first()
    print(product_dep)
    product_sav = SavingProducts.objects.filter(fin_prdt_nm=pdt_name).first()
    if product_dep:
        product = product_dep
        type = 'dep'
        productId = product.fin_prdt_cd
    elif product_sav:
        product = product_sav
        type = 'sav'
        productId = product.fin_prdt_cd
    else:
        # 두 모델에서 모두 해당 상품명을 찾지 못한 경우
        raise Http404("Product not found")
    print(type, productId)
    response_data = {
        'type':type, 
        'productId':productId
        }
    return Response(response_data)
    # return Response({ 'message': 'okay!'})


@api_view(['GET'])
def one_dep_opt(request, opt_pk):
    print(opt_pk)
    option = DepositOptions.objects.get(pk=opt_pk)
    print(option)
    serializer = OneDepOptSerializer(option)
    return Response(serializer.data)


@api_view(['GET'])
def one_sav_opt(request, opt_pk):
    option = SavingOptions.objects.get(pk=opt_pk)
    serializer = OneSavOptSerializer(option)
    return Response(serializer.data)

# 예금 랜덤 캐러셀
@api_view(['GET'])
def random_product_dep(request):
    all_pdt_dep = DepositProducts.objects.all()

    # 정렬해서 -> 셔플해서 랜덤으로 세우기
    pdt_dep = all_pdt_dep.order_by(F('pk').desc())
    # print(pdt_dep,'?')
    pdt_random_dep = list(pdt_dep)
    shuffle(pdt_random_dep)  # 섞음
    print(pdt_random_dep)
    selected_pdt_dep = pdt_random_dep[:20]

    serializer_dep = DepositProductsSerializer(selected_pdt_dep, many=True)
    return Response(serializer_dep.data)


# 적금 랜덤 캐러셀
@api_view(['GET'])
def random_product_sav(request):
    all_pdt_sav = SavingProducts.objects.all()

    # 정렬해서 -> 셔플해서 랜덤으로 세우기
    pdt_sav = all_pdt_sav.order_by(F('pk').desc())
    print('ok?')
    pdt_random_sav = list(pdt_sav)
    shuffle(pdt_random_sav)  # 섞음
    
    selected_pdt_sav = pdt_random_sav[:20]

    serializer_sav = SavingProductsSerializer(selected_pdt_sav, many=True)
    return Response(serializer_sav.data)

