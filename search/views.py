from django.shortcuts import render
from articles.utils import search


def search_view(request):
    result = search(request)
    template_name = 'search/results.html'
    context = {
        'title': f'Результат поиска',
        'queryset': result
    }
    if request.htmx:
        template_name = 'search/partials/results.html'
        context['queryset'] = result[:5]
    return render(request, template_name=template_name, context=context)

