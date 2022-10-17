from django.urls import path, include
from .views import (
    home,
    detail_article,
    create_article,
    delete_article,
)

urlpatterns = [
    path('', home, name='home_page'),
    path('recipes/', include('recipes.urls')),
    path('article/<slug:slug>/', detail_article, name='detail_article_page'),
    path('create-article/', create_article, name='create_article_page'),
    path('article/<slug:slug>/delete/', delete_article, name='delete_article')
]
