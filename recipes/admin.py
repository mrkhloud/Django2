from django.contrib import admin

from .models import *


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0
    readonly_fields = ('quantity_float', 'as_mks', 'as_imperial',)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    readonly_fields = ('publish', 'update',)
    raw_id_fields = ('user',)


admin.site.register(Recipe, RecipeAdmin)
