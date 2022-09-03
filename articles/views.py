from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .utils import *
from .forms import *


def home(request):
    articles = get_articles_for_home()
    context = {
        'title': 'Домашняя страница',
        'articles': articles,
    }
    return render(request, 'home.html', context)


def detail_article(request, slug):
    article = get_detail_article(slug)
    context = {
        'title': article.title,
        'article': article
    }
    return render(request, 'detail_article.html', context=context)


def article_search(request):
    query = get_query_for_search(request)
    title = get_title_for_search(query)
    articles = get_articles_for_search(query)
    context = {
        'title': title,
        'articles': articles
    }
    return render(request, 'search_article.html', context)


@login_required
def create_article(request):
    form = ArticleForm(request.POST or None)
    context = {
        'title': 'Создание новой статьи',
        'form': form,
    }
    if form.is_valid():
        create_obj(request, form)
        return redirect('home_page')
    return render(request, 'create_article.html', context=context)
