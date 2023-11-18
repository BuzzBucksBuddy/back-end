from django.urls import path
from . import views

app_name = 'maps'
urlpatterns = [
    path('deposits/', views.get_all_deposit_products),
    path('savings/', views.get_all_saving_products),
    path('deposits/<str:kor_co_nm>/', views.get_deposit_products),
    path('savings/<str:kor_co_nm>/', views.get_saving_products),
]
