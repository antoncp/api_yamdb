from django.contrib import admin

from .models import Category, Genre


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
