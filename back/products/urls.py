from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('save-data/', views.save_data),  # 상품/옵션 데이터 저장
    path('product-list/', views.product_list),  # 상품 전체 조회
    path('product-options/<str:fin_prdt_cd>/', views.product_options),  # 특정 상품의 옵션 조회
]
