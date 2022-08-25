from django.utils.text import slugify
from transliterate import translit


def my_slugify(value: str) -> str:
    value = translit(value, reversed=True)
    return value
