from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .services import get_user_recipes
from .utils import *
from .form import *
from .models import *


@login_required()
def recipe_list_view(request):
    user = request.user
    recipes = get_user_recipes(user)
    context = {
        'title': f'Список всех рецептов пользователя {user}',
        'objects_list': recipes
    }
    return render(request, 'list.html', context=context)


@login_required()
def recipe_detail_view(request, id=None):
    hx_url = reverse('detail_hx_recipe', kwargs={'id': id})
    context = {
        'hx_url': hx_url
    }
    return render(request, 'detail.html', context=context)


@login_required()
def recipe_detail_hx_view(request, id=None):
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        context = {
            'obj_is_none': True
        }
        return render(request, 'base.html', context=context)
    context = {
        'title': f'Подробная страница рецепта {obj.name}',
        'object': obj,
    }
    return render(request, 'partials/detail.html', context=context)


@login_required()
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        'title': 'Создание нового рецепта',
        'form': form,
    }
    if form.is_valid():
        recipe_create(request, form)
    return render(request, 'create-update.html', context=context)


@login_required()
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    context = {
        'title': 'Редактирование рецепта',
        'form': form,
        'object': obj,
    }
    if form.is_valid():
        recipe_create(request, form)
    if request.htmx:
        return render(request, 'partials/form.html', context=context)
    return render(request, 'create-update.html', context=context)



