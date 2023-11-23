from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('products-data/', views.products_data),  # 상품/옵션 데이터 저장

    path('deposit-list/<str:kor_co_nm>/', views.deposit_filtered),  # 예금 상품 은행별 조회
    path('saving-list/<str:kor_co_nm>/', views.saving_filtered),  # 적금 상품 은행별 조회
    path('deposit-categorize/<str:fin_prdt_cd>/<int:save_trm>/', views.deposit_categorize),  # 예금 상품 옵션 기간별 조회
    path('saving-categorize/<str:fin_prdt_cd>/<int:save_trm>/<str:rsrv_type_nm>/', views.saving_categorize),  # 적금 상품 옵션 기간/유형별 조회

    path('deposit-product/<str:fin_prdt_cd>/', views.deposit_product),  # 예금 상품 단일 조회
    path('saving-product/<str:fin_prdt_cd>/', views.saving_product),  # 적금 상품 단일 조회
    path('deposit-options/<str:fin_prdt_cd>/', views.deposit_options),  # 예금 상품의 옵션 조회
    path('saving-options/<str:fin_prdt_cd>/', views.saving_options),  # 적금 상품의 옵션 조회

    path('deposit-options/<str:option_pk>/join/', views.become_my_dep_option),  # 예금 상품 가입
    path('saving-options/<str:option_pk>/join/', views.become_my_sav_option),  # 적금 상품 가입
    
    path('goDetail/<str:pdt_name>/', views.find_product),

    path('one-dep-opt/<int:opt_pk>/', views.one_dep_opt),
    path('one-sav-opt/<int:opt_pk>/', views.one_sav_opt),
]