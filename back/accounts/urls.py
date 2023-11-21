from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/', views.my_profile),
    path('favorites/', views.favorite_category),
    path('favorites/<int:favorite_pk>/select/', views.favorite_select),


    path('users-age/', views.users_age),

    path('users_favorite/<int:favorite_pk>/', views.users_favorite),
]