import pint
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse

from .validators import validate_unit_of_measure
from .utils import number_str_to_float


class RecipeQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == '':
            return self.none()
        lookups = Q(name__iregex=query)
        return self.filter(lookups)


class RecipeManager(models.Manager):
    def get_query_set(self):
        return RecipeQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_query_set().search(query)


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='Хозяин рецепта',
                             blank=True, null=True)
    name = models.CharField(max_length=220, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    publish = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')
    active = models.BooleanField(default=True, verbose_name='Могут видеть другие пользователи?')

    objects = RecipeManager()

    @property
    def title(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail_recipe', kwargs={'id': self.pk})

    def get_update_url(self):
        return reverse('update_recipe', kwargs={'id': self.pk})

    def get_delete_url(self):
        return reverse('delete_recipe', kwargs={'id': self.pk})

    def get_ingredients(self):
        return self.recipeingredient_set.all()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    quantity = models.CharField(max_length=50, verbose_name='Количество')
    quantity_float = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, verbose_name='Мера счёта', validators=(validate_unit_of_measure,))
    directions = models.TextField(blank=True, null=True)
    publish = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')
    active = models.BooleanField(default=True, verbose_name='Могут видеть другие пользователи?')

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингридиенты рецепта'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.recipe.get_absolute_url()

    def get_parent_id_and_id(self):
        kwargs = {
            'parent_id': self.recipe.id,
            'id': self.id
        }
        return kwargs

    def get_hx_update_url(self):
        return reverse('hx-update-ingredient', kwargs={
            'parent_id': self.recipe.id,
            'id': self.id
        })

    def get_delete_url(self):
        return reverse('delete_recipe_ingredient', kwargs={
            'parent_id': self.recipe.id,
            'id': self.id
        })

    def convert_to_system(self, system='mks'):
        if self.quantity_float is not None:
            ureg = pint.UnitRegistry(system=system)
            measurement = self.quantity_float * ureg[self.unit]
            return measurement
        return None

    def as_mks(self):
        measurement = self.convert_to_system(system='mks')
        return measurement.to_base_units()

    def as_imperial(self):
        measurement = self.convert_to_system(system='imperial')
        return measurement.to_base_units()

    def save(self, *args, **kwargs):
        qty = str(self.quantity)
        qty_float, qty_float_success = number_str_to_float(qty)
        if qty_float_success:
            self.quantity_float = qty_float
        super().save(*args, **kwargs)
