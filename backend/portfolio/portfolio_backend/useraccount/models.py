import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.conf import settings
from django.db import models


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('You must enter an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='uploads/avatars', blank=True, null=True)
    about = models.TextField(blank=True, null=True) #This will be a rich text, that will be sent from the frontend
    links = models.JSONField(default=list ,blank=True, null=True)