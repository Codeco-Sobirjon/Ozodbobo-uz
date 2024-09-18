from django.db import models
from django.utils.translation import gettext_lazy as _
from django_restful_translator.models import TranslatableModel
from django.core.exceptions import ValidationError


def validate_video_size(value):
    file_size = value.size
    max_size_mb = 70 * 1024 * 1024  # 70 MB in bytes
    min_size_mb = 2 * 1024 * 1024  # 10 MB in bytes

    if file_size > max_size_mb:
        raise ValidationError(_("Максимальный размер загружаемого файла составляет 70 МБ."))
    elif file_size < min_size_mb:
        raise ValidationError(_("Минимальный размер загружаемого файла составляет 2 МБ."))


class Categories(models.Model):
    name = models.CharField(_("Название категории"), max_length=500, null=True, blank=True)

    translatable_fields = ['name']

    objects = models.Manager()

    def __str__(self):
        return self.name  # Ensure that the name is returned here

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        db_table = 'categories'


class Blog(models.Model):
    title = models.CharField(_('Название'), max_length=500, null=True, blank=True)
    description = models.TextField(_('Описание'), null=True, blank=True)
    is_seen = models.IntegerField(default=0, verbose_name="Просмотрено")
    category = models.ManyToManyField(Categories, null=True, blank=True,
                                      related_name="Category", verbose_name=_('Выбрать категорию'))
    created_at = models.DateField(auto_now_add=True, verbose_name=_("Дата публикации"))
    url = models.URLField(verbose_name="URL", null=True, blank=True)
    video = models.URLField(verbose_name='URL-видео', null=True, blank=True)
    translatable_fields = ['title', 'description']

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Блог")
        verbose_name_plural = _("Блоги")
        ordering = ['created_at']
        db_table = 'blog'


class BlogImage(models.Model):
    image = models.ImageField(upload_to='images', null=True, blank=True, verbose_name=_("Изображение"))
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True, related_name="blogImage",
                             verbose_name=_('Блоги'))

    def __str__(self):
        return self.blog.title

    objects = models.Manager()

    class Meta:
        verbose_name = _("Блог")
        verbose_name_plural = _("Блоги")
        db_table = 'blog_image'


class BlogComment(models.Model):
    full_name = models.CharField(_("Полное имя фамилия"), max_length=250, null=True, blank=True)
    phone = models.CharField(_("Номер телефона"), max_length=250, null=True, blank=True)
    comment = models.TextField(verbose_name="Объяснение", null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True, related_name="blogCommant",
                             verbose_name=_('Блоги'))
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("Комментарии в блоге")
        verbose_name_plural = _("Комментарий в блоге")
        db_table = 'blog_comment'
