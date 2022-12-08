from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

class News(models.Model):
    header = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    url = models.SlugField()
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField()
    created_at = models.DateField(default=timezone.now)
    tag = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Debuts(models.Model):
    header = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    url = models.SlugField()
    content = RichTextUploadingField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Дебют'
        verbose_name_plural = 'Дебюты'

class Lessons(models.Model):
    header = models.CharField(max_length=200)
    url = models.SlugField()
    description = models.CharField(max_length=200)
    content = RichTextUploadingField()

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Articles(models.Model):
    header = models.CharField(max_length=200)
    url = models.SlugField()
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField()

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateField(default=timezone.now)

    # Сортировка комментариев
    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    # Меняем отображение в админке
    def __str__(self):
        return self.text