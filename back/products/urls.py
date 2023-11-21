from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('products-data/', views.products_data),  # 상품/옵션 데이터 저장
    path('deposit-list/', views.deposit_list),  # 예금 상품 전체 조회
    path('saving-list/', views.saving_list),  # 적금 상품 전체 조회
    path('deposit-product/<str:fin_prdt_cd>/', views.deposit_product),  # 예금 상품 단일 조회
    path('saving-product/<str:fin_prdt_cd>/', views.saving_product),  # 적금 상품 단일 조회
    path('deposit-options/<str:fin_prdt_cd>/', views.deposit_options),  # 예금 상품의 옵션 조회
    path('saving-options/<str:fin_prdt_cd>/', views.saving_options),  # 적금 상품의 옵션 조회

    path('deposit-list/<str:kor_co_nm>/', views.deposit_filtered),  # 예금 상품 은행별 조회
    path('saving-list/<str:kor_co_nm>/', views.saving_filtered),  # 적금 상품 은행별 조회
    path('deposit-categorize/<str:fin_prdt_cd>/<int:save_trm>/', views.deposit_categorize),
    path('saving-categorize/<str:fin_prdt_cd>/<int:save_trm>/<str:rsrv_type_nm>/', views.saving_categorize),
]
