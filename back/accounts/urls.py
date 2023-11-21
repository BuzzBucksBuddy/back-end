from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/', views.my_profile),
    path('favorites/', views.favorite_category),
    path('favorites/<int:favorite_pk>/select/', views.favorite_select),
    path('users_favorite/', views.users_favorite),
]