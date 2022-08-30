from django.db import models
from django.urls import reverse
from .services import slugify


class Article(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(blank=True, null=True)
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_article_page', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
