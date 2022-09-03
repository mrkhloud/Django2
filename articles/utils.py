from django.http import Http404
from django.shortcuts import redirect

from .models import Article


def get_detail_article(slug):
    try:
        return Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise Http404
    except Article.MultipleObjectsReturned:
        return Article.objects.filter(slug=slug).first()
    except:
        raise Http404


def get_articles_for_home():
    return Article.objects.all()


def get_query_for_search(request):
    try:
        query = request.GET.get('q')
    except:
        query = None
    return query


def get_title_for_search(query):
    title = f'Результат поиск "{query}"'
    if query is None or query == '':
        title = 'Пустой запрос'
    return title


def get_articles_for_search(query):
    return Article.objects.search(query)


def create_obj(request, form):
    article = form.save(commit=False)
    article.user = request.user
    article.save()
