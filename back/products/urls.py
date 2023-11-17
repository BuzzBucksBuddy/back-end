from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('products-data/', views.products_data),  # 상품/옵션 데이터 저장
    path('deposit-list/', views.deposit_list),  # 예금 상품 전체 조회
    path('saving-list/', views.saving_list),  # 적금 상품 전체 조회
    path('deposit-options/<str:fin_prdt_cd>/', views.deposit_options),  # 예금 상품의 옵션 조회
    path('saving-options/<str:fin_prdt_cd>/', views.saving_options),  # 적금 상품의 옵션 조회
]
