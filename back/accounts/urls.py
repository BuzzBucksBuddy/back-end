from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/', views.my_profile),
    path('favorites/', views.favorite_category),
    path('favorites/<int:favorite_pk>/select/', views.favorite_select),

    # path('dep_users/<str:fin_prdt_cd>/', views.dep_users),
    # path('sav_users/<str:fin_prdt_cd>/', views.sav_users),

    path('users_age/<int:age>/', views.users_age),
    path('users_money/<int:money>/', views.users_money),
    path('users_salary/<int:salary>/', views.users_salary),
    path('users_mbti/<str:mbti>/', views.users_mbti),
    path('users_favorite/<int:favorite_pk>/', views.users_favorite),

    path('my_intr_rate_graph/', views.my_intr_rate_graph),
    path('my_products/', views.my_products),
    path('mileage/', views.add_mileage),
]