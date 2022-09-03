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
        'object_ingredients': obj.recipeingredient_set.all()
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
        context['message'] = 'Данные сохранены!'
    return render(request, 'create-update.html', context=context)


@login_required()
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    RecipeIngredientFormSet = modelformset_factory(
        RecipeIngredient,
        form=RecipeIngredientForm,
        extra=0
    )
    qs = obj.recipeingredient_set.all()
    formset = RecipeIngredientFormSet(request.POST or None, queryset=qs)
    context = {
        'title': 'Редактирование рецепта',
        'form': form,
        'formset': formset,
        'object': obj
    }
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.user = request.user
        parent.save()
        for form in formset:
            child = form.save(commit=False)
            child.recipe = parent
            child.save()
        context['message'] = 'Данные обновлены!'
    return render(request, 'create-update.html', context=context)
