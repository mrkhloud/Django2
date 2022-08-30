from django.conf import settings
from django.db import models


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Хозяин рецепта')
    name = models.CharField(max_length=220, verbose_name='Название рецепта')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    publish = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')
    active = models.BooleanField(default=True, verbose_name='Видят другие пользователи?')


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    quanity =  models.CharField(max_length=50, verbose_name='Количество')
    unit = models.CharField(max_length=50, verbose_name='Мера счёта')
    directions = models.TextField(blank=True, null=True)
    publish = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')
    active = models.BooleanField(default=True, verbose_name='Видят другие пользователи?')
