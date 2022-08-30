from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from .services import my_slugify


User = settings.AUTH_USER_MODEL


class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == '':
            return self.none()
        lookups = Q(title__iregex=query) | Q(content__iregex=query) | Q(slug__iregex=query)
        return self.filter(lookups)


class ArticleManager(models.Manager):
    def get_query_set(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_query_set().search(query)


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             blank=True, null=True)
    title = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = ArticleManager()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_article_page', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = my_slugify(self.title)
        super().save(*args, **kwargs)
