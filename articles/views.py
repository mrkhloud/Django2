from django.db.models import Q
from django.http import Http404
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


def detail_article(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise Http404
    except Article.MultipleObjectsReturned:
        article = Article.objects.filter(slug=slug).first()
    except:
        raise Http404
    context = {
        'title': article.title,
        'article': article
    }
    return render(request, 'detail_article.html', context=context)


def article_search(request):
    try:
        query = request.GET.get('q')
    except:
        query = None
    lookups = Q(title__iregex=query) | Q(content__iregex=query) | Q(slug__iregex=query)
    if query is None or query == '':
        title = 'Пустой запрос'
        articles = Article.objects.all()
    else:
        title = f'Результат запроса "{query}"'
        articles = Article.objects.filter(lookups)
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
        article = form.save()
        context['article'] = article
        context['created'] = True
    return render(request, 'create_article.html', context=context)
