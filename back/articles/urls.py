from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.article_create),
    path('list/', views.article_list),
    path('list/<int:product_pk>/<int:bank_pk>/', views.article_categorize),

    path('list/search/<str:field>/<str:input>/', views.article_search),

    path('<int:article_pk>/detail/', views.article_detail),
    path('<int:article_pk>/control/', views.article_control),
    path('<int:article_pk>/likes/', views.article_like),

    path('<int:article_pk>/comments/', views.comment_create),
    path('<int:article_pk>/comments_list/', views.comment_list),
    path('<int:article_pk>/comments/<int:comment_pk>/', views.comment_control),
    path('<int:article_pk>/comments/<int:comment_pk>/likes/', views.comment_like),

    path('category/products/', views.product_category_list),
    path('category/banks/', views.bank_category_list),
]
