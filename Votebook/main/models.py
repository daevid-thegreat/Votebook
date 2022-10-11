from email.policy import default
from secrets import choice
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from requests import options
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
from Votebook.settings import AUTH_USER_MODEL

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

    def create_superuser(self, email, password, **other_fields ):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('superuser must be assigned is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be assigned is_superuser=True')

        return self.create_user(email, password, **other_fields)



class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, default="None")
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = UserprofileManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Subject(models.Model):
    id_subject = models.CharField(default=uuid.uuid4, max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length= 255)


    def __str__(self):
        return self.party_name

    @property
    def total_votes(self):
        total = self.options.aggregate(models.Sum('votes'))['votes__sum']
        return total

class Option(models.Model):
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    option_name = models.CharField(max_length= 150)
    votes = models.BigIntegerField()

    def __str__(self):
        return self.subject


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



    