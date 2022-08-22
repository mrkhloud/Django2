from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Article
from .forms import ArticleForm


def home(request):
    articles = Article.objects.all()
    context = {
        'title': 'Домашняя страница',
        'articles': articles,
    }
    return render(request, 'home.html', context)


def detail_article(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'title': article.title,
        'article': article
    }
    return render(request, 'detail_article.html', context=context)


def article_search(request):
    pk = request.GET['q']
    article = Article.objects.get(title=pk)
    context = {
        'title': article.title,
        'article': article
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
        article = form.save()
        context['article'] = article
        context['created'] = True
    return render(request, 'create_article.html', context=context)
