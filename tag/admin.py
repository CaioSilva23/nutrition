from django.contrib import admin
from tag.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'slug')
    search_fields = ('name', 'id')
    list_per_page = 10
    list_editable = ('name',)
    ordering = ('-id',)

    # gera o slug automaticamente pelo name
    prepopulated_fields = {
        'slug': ('name',),
    }
