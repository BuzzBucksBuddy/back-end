from django.contrib import admin
from .models import Article, Comment, ArticleBankCategory, ArticleProductCategory

# Register your models here.
admin.site.register((Article, Comment, ArticleBankCategory, ArticleProductCategory,))
