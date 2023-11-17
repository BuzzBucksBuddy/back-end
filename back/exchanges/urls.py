from django.urls import path
from . import views

app_name = 'exchanges'
urlpatterns = [
    path('save-exchange-rates/', views.save_exchange_rates),     # 저장
    path('<str:country>/<str:category>/', views.find_country_info),
    path('', views.exchange_all),                                    # 환율정보 조회
]
