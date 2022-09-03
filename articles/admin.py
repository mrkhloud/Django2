from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('user',)
    readonly_fields = ('publish', 'update',)


admin.site.register(Article, ArticleAdmin)
