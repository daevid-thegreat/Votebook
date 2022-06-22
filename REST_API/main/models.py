from secrets import choice
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

from REST_API.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL


class UserprofileManager(BaseUserManager):

    def create_user(self, email, password, **other_fields ):
        
        if not email:
            raise ValueError("you must add an email")

        email = self.normalize_email(email)
        user = self.model(email =email, password = password, **other_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user.email

    def create_candidate(self, email, password, **other_fields ):
        user = self.create_user(email, password, **other_fields)
        user.is_candidate = True
        user.save(using=self._db)

        return user.email

    def create_superuser(self, email, password, **other_fields ):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_candidate', False)

        if other_fields.get('is_staff') is not True:
            raise ValueError('superuser must be assigned is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be assigned is_superuser=True')

        return self.create_user(email, password, **other_fields)

choices = [
    ('President', 'President'),
    ('Prime Minister', 'Prime Minister'),
    ('Head of State', 'Head of State'),
    ('Honorable', 'Honorable'),
]

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_candidate = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    party = models.ForeignKey('Party', on_delete=models.CASCADE, null=True)
    votes = models.IntegerField(default=0)
    position = models.CharField(max_length=255, choices=choices, default='Honorable')


    objects = UserprofileManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Party(models.Model):
    party_name = models.CharField(max_length=100)

    def __str__(self):
        return self.party_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



    