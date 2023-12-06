from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')


class Post (models.Model):
    TYPE = (
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('buyers', 'Торговцы'),
        ('gildemaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    )

    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.TextField()
    category = models.ForeignKey(Category, max_length=11, choices=TYPE, default='tank', on_delete=models.CASCADE)
    upload = models.FileField(upload_to='media')


class UserResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reply_user')
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reply')
    status = models.BooleanField(default=False)


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
