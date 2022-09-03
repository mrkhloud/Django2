from django import forms

from .models import *


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                'placeholder': f'Recipe {field}',
                'class': f'recipe-{field}-field'
            }
            if 'Textarea' in str(self.fields[field].widget):
                new_data['rows'] = '3'
            self.fields[field].widget.attrs.update(new_data)

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'directions',)


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ('name', 'quantity', 'unit',)
