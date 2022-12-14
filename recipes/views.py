from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
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
    except Exception as e:
        obj = None
        print(e)
    if obj is None:
        context = {
            'obj_is_none': True
        }
        return render(request, 'base.html', context=context)
    context = {
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
        obj = recipe_create(request, form)
        if request.htmx:
            headers = {
                'HX-Redirect': obj.get_absolute_url()
            }
            return HttpResponse('-', headers=headers)
    return render(request, 'create-update.html', context=context)


@login_required()
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    new_ingredient_url = reverse('hx-new-ingredient', kwargs={'parent_id': obj.id})
    context = {
        'title': 'Редактирование рецепта',
        'form': form,
        'object': obj,
        'new_ingredient_url': new_ingredient_url
    }
    if form.is_valid():
        recipe_create(request, form)
    if request.htmx:
        return render(request, 'partials/form.html', context=context)
    return render(request, 'create-update.html', context=context)


@login_required()
def recipe_ingredient_update_hx_view(request, parent_id=None, id=None):
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except Exception as e:
        parent_obj = None
        print(e)
    if parent_obj is None:
        context = {
            'obj_is_none': True
        }
        return render(request, 'base.html', context=context)
    obj = None
    if id is not None:
        try:
            obj = RecipeIngredient.objects.get(id=id, recipe=parent_obj)
        except Exception as e:
            obj = None
            print(e)
    form = RecipeIngredientForm(request.POST or None, instance=obj)
    url = obj.get_hx_update_url() if obj is not None else reverse('hx-new-ingredient', kwargs={'parent_id': parent_id})
    context = {
        'object': obj,
        'form': form,
        'url': url
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if obj is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, 'partials/ingredient-inline.html', context=context)
    return render(request, 'partials/ingredient-form.html', context=context)


@login_required()
def recipe_delete_view(request, id=None):
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except Exception as e:
        obj = None
        print(e)
    if obj is None:
        if request.htmx:
            return HttpResponse('HTMX REQUEST!')
        raise Http404()
    if request.method == 'POST':
        obj.delete()
        success_url = reverse('list_recipe')
        if request.htmx:
            headers = {
                'HX-Redirect': success_url
            }
            return HttpResponse('HTMX REDIRECT!', headers=headers)
        return redirect(success_url)
    context = {
        'object': obj,
        'title': f'Удаление {obj.name}'
    }
    return render(request, 'delete.html', context=context)


@login_required()
def recipe_ingredient_delete_view(request, parent_id=None, id=None):
    try:
        obj = RecipeIngredient.objects.get(recipe__id=parent_id, id=id)
    except Exception as e:
        obj = None
        print(e)
    if obj is None:
        if request.htmx:
            return HttpResponse('HTMX REQUEST!')
        raise Http404()
    if request.method == 'POST':
        obj.delete()
        success_url = reverse('detail_recipe', kwargs={'id': parent_id})
        if request.htmx:
            return HttpResponse('HTMX REDIRECT!')
        return redirect(success_url)
    context = {
        'object': obj,
        'title': f'Удаление {obj.name}'
    }
    return render(request, 'delete.html', context=context)
