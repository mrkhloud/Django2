from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

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
        'object': obj
    }
    if form.is_valid():
        recipe_create(request, form)
    if request.htmx:
        return render(request, 'partials/forms.html', context=context)
    return render(request, 'create-update.html', context=context)


@login_required()
def recipe_ingredients_update_hx_view(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404()
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
        context = {
            'obj_is_none': True
        }
        return render(request, 'base.html', context=context)
    if id is not None:
        try:
            obj = RecipeIngredient.objects.get(id=id, recipe=parent_obj)
        except:
            obj = None
    form = RecipeIngredientForm(request.POST or None, instance=obj)
    url = reverse('ingredient_hx_recipe', kwargs={'parent_id': parent_obj.pk})
    if obj:
        url = obj.get_hx_edit_url()
    context = {
        'title': f'Подробная страница рецепта {obj.name}',
        'url': url,
        'object': obj,
        'form': form
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if obj is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, 'partials/ingredient-inline.html', context=context)
    return render(request, 'partials/ingredient-form.html', context=context)
