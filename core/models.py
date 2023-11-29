import hashlib

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser
from django.db import models

from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)

        if not email and not user.is_superuser:
            raise ValueError('Email must be set')

        # Validación adicional para usuarios normales
        if not user.is_superuser:
            if not user.dni or not user.age:
                raise ValueError('DNI and Age must be set for non-superuser users.')

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


# Create your models here.
class CustomUser(AbstractUser):
    photo = models.ImageField(verbose_name="photo", upload_to='profile_photos', blank=True, null=True)
    age = models.DateField(verbose_name="Date", blank=True, null=True)
    dni = models.CharField(max_length=8, verbose_name="DNI", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Last Update")

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def gravatar_url(self, pixelSize=150):
        email_hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

        # API Gravatar
        return f"https://www.gravatar.com/avatar/{email_hash}?s={pixelSize}&d=identicon"

    @classmethod
    def get_user(cls, user_id):
        try:
            return cls.objects.get(pk=user_id)
        except cls.DoesNotExist:
            return None
