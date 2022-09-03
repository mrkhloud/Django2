from .models import Recipe


def get_user_recipes(user):
    qs = Recipe.objects.filter(user=user)
    return qs