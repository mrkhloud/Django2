# Generated by Django 4.1 on 2022-09-03 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import recipes.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=220, verbose_name='Название рецепта')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('directions', models.TextField(blank=True, null=True)),
                ('publish', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
                ('active', models.BooleanField(default=True, verbose_name='Могут видеть другие пользователи?')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Хозяин рецепта')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=220, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('quantity', models.CharField(max_length=50, verbose_name='Количество')),
                ('quantity_float', models.FloatField(blank=True, null=True)),
                ('unit', models.CharField(max_length=50, validators=[recipes.validators.validate_unit_of_measure], verbose_name='Мера счёта')),
                ('directions', models.TextField(blank=True, null=True)),
                ('publish', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
                ('active', models.BooleanField(default=True, verbose_name='Могут видеть другие пользователи?')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
            ],
            options={
                'verbose_name': 'Ингредиент рецепта',
                'verbose_name_plural': 'Ингридиенты рецепта',
            },
        ),
    ]
