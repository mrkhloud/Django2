from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_article_page', kwargs={'pk': self.pk})
