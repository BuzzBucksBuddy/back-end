from rest_framework.response import Response
from rest_framework.decorators import api_view

from products.models import SavingProducts, DepositProducts
from products.serializers import SavingProductsSerializer, DepositProductsSerializer


@api_view(['GET'])
def get_all_deposit_products(request):
    if request.method == 'GET':
        dep_banks = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(dep_banks, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_all_saving_products(request):
    if request.method == 'GET':
        sav_banks = SavingProducts.objects.all()
        serializer = SavingProductsSerializer(sav_banks, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_deposit_products(request, kor_co_nm):
    if request.method == 'GET':
        dep_banks = DepositProducts.objects.filter(kor_co_nm=kor_co_nm)
        serializer = DepositProductsSerializer(dep_banks, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_saving_products(request, kor_co_nm):
    if request.method == 'GET':
        sav_banks = SavingProducts.objects.filter(kor_co_nm=kor_co_nm)
        serializer = SavingProductsSerializer(sav_banks, many=True)
        return Response(serializer.data)
