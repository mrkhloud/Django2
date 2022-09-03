from django.urls import path

from .views import *

urlpatterns = [
    path('', recipe_list_view, name='list_recipe'),
    path('<int:id>/', recipe_detail_view, name='detail_recipe'),
    path('hx/<int:id>/', recipe_detail_hx_view, name='detail_hx_recipe'),
    path('create/', recipe_create_view, name='create_recipe'),
    path('<int:id>/update/', recipe_update_view, name='update_recipe'),
]