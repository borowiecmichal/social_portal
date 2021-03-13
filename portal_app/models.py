import datetime

from django.db import models
from django.conf import settings
from django.utils.text import slugify


class AdditionalInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    motorcycle = models.CharField(max_length=64, default=None, null=True)
    date_of_birth = models.DateField(default=None, null=True)
    city = models.CharField(max_length=64, default=None, null=True)

    @property
    def age(self):
        return (datetime.datetime.now().date()-self.date_of_birth).days//365


class Post(models.Model):
    content = models.TextField(verbose_name='Treść')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_add = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    group = models.ForeignKey('Groupe', on_delete=models.SET_DEFAULT, null=True, default=None)

    class Meta:
        ordering = ['-date_add']


class Photo(models.Model):
    photo = models.ImageField(blank=True, verbose_name='Zdjęcie')
    description = models.CharField(max_length=255, null=True, default=None, verbose_name='Opis')
    date_add = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, default=None)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_add = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=64)
    upper_class_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)
    def __str__(self):
        return self.name

class Groupe(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    slug = models.SlugField(max_length=128, null=True, default=None, unique=True)

    def get_categories_list(self):
        cat = self.category
        path = []
        while cat.upper_class_category:
            path.append(cat.upper_class_category.name)
            cat = cat.upper_class_category
        path.reverse()
        path = '➝'.join(path)

        return path

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Messages(models.Model):
    content = models.TextField()
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='from_msg')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to_msg')
    date = models.DateTimeField(auto_now_add=True)
