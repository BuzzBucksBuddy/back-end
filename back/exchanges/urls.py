from django.urls import path
from . import views

app_name = 'exchanges'
urlpatterns = [
    path('save-exchange-rates/', views.save_exchange_rates),     # 저장
    path('', views.exchange),                                    # 환율정보 조회
]
