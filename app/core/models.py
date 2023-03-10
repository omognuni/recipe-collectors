from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class Ingredient(models.Model):
    name = models.CharField(max_length=300)
    number = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('recipe', 'name')


class Recipe(models.Model):
    index = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=300)
    process = models.TextField(default='')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        '''유저 생성'''
        if not email:
            raise ValueError('메일을 입력하세요')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        '''superuser 생성'''
        user = self.create_user(email, password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''email을 username으로 사용하는 유저 모델'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
