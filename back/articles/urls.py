from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.article_list),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/comments/', views.comment_list),
    path('category/products/', views.product_category_list),
    path('category/banks/', views.bank_category_list),
]
