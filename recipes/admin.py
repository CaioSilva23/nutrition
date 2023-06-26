from django.contrib import admin
from .models import Category, Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'is_published', 'category', 'author')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_filter = ('category', 'author', 'is_published')
    list_per_page = 10
    list_editable = ('is_published', )
    ordering = ('-id', )
    prepopulated_fields = {
        'slug': ('title',),
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
