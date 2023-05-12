from django.contrib import admin

from .models import Category, Comment, Genre, Title, Review


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'display_genres',
        'category'
    )
    search_fields = ('name', 'description')
    list_filter = ('name', 'year')
    empty_value_display = '-empty-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "score",
        "title_id",
        "author",
        "pub_date"
    )
    search_fields = ("text",)
    list_filter = ("pub_date", "title_id")
    empty_value_display = "-empty-"


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "title_id",
        "review_id",
        "author",
        "pub_date"
    )
    search_fields = ("text",)
    list_filter = ("pub_date", "title_id")
    empty_value_display = "-empty-"


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
