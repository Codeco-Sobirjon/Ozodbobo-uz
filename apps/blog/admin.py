from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import Categories, Blog, BlogImage, BlogComment
from django_restful_translator.admin import TranslationInline

class ImageMixin:
    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
        return ""
    image_tag.short_description = 'Показать изображение'


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


class BlogImageInline(admin.StackedInline, ImageMixin):
    model = BlogImage
    extra = 1
    readonly_fields = ('image_tag',)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_seen', 'created_at', 'get_categories')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'category')
    ordering = ('-created_at',)
    inlines = [BlogImageInline]

    # Adding the video field to be displayed in the admin form
    fields = ('title', 'description', 'is_seen', 'category', 'video')

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    get_categories.short_description = _("Категории")

    class Meta:
        verbose_name = _("Блог")
        verbose_name_plural = _("Блоги")


class BlogImageAdmin(admin.ModelAdmin, ImageMixin):
    list_display = ('blog', 'image_tag')
    search_fields = ('blog__title',)
    readonly_fields = ('image_tag',)

    class Meta:
        verbose_name = "Blog Rasm"
        verbose_name_plural = "Blog Rasmlar"


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone']
    search_fields = ['full_name']


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
# admin.site.register(BlogImage, BlogImageAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = _("Озодбобо")
admin.site.site_title = _("Административный портал")
admin.site.index_title = _("Добро пожаловать в персонализированную панель управления")
