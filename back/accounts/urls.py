from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/', views.my_profile),
    path('favorites/', views.favorite_category),
    path('favorites/<int:favorite_pk>/select/', views.favorite_select),

    path('dep_users/<str:fin_prdt_cd>/', views.dep_users),
    path('sav_users/<str:fin_prdt_cd>/', views.sav_users),

    path('users_age/<int:age>/', views.users_age),
    path('users_money/<int:money>/', views.users_money),
    path('users_salary/<int:salary>/', views.users_salary),

    path('users_favorite/', views.users_favorite),
]