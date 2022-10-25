from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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


@login_required
def delete_article(request, slug=None):
    article = Article.objects.get(slug=slug, user=request.user)
    if article is None:
        if request.htmx:
            return HttpResponse('Статейка была удалена!')
        raise Http404()
    if request.method == 'POST':
        article.delete()
        success_url = reverse('home_page')
        if request.htmx:
            headers = {
                'HX-Redirect': success_url
            }
            return HttpResponse('йцу', headers=headers)
        return redirect('home_page')
    context = {
        'object': article,
        'title': f'Удаление {article.name}'
    }
    return render(request, 'delete.html', context=context)