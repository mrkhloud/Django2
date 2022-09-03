# Generated by Django 4.1 on 2022-09-03 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='Заголовок')),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField(verbose_name='Содержимое')),
                ('publish', models.DateTimeField(auto_now_add=True, verbose_name='Время и дата публикации')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Время и дата последнего редактирования')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор статьи')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]
