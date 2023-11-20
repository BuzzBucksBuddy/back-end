from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('<str:user_id>/', views.my_profile),
]