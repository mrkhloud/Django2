from django.urls import path, include
from .views import (
    home,
    detail_article,
    article_search,
    create_article,
)


urlpatterns = [
    path('', home, name='home_page'),
    path('recipes/', include('recipes.urls')),
    path('article/<slug:slug>/', detail_article, name='detail_article_page'),
    path('result/', article_search, name='res_search_page'),
    path('create-article/', create_article, name='create_article_page')
]