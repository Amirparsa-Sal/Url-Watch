from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password):
        if not email:
            raise ValueError('Users must have an email address.')
        if not password:
            raise ValueError('Users must have a password.')

        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name, last_name=last_name)
        user.is_active = True
        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(self,email, password, first_name=None, last_name=None):
        user = self.create_user(email, first_name, last_name, password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False) #if the account is activated
    is_staff = models.BooleanField(default=False) #if is admin

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

class Url(models.Model):
    url = models.URLField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    failed_times = models.IntegerField(default=0)
    threshold = models.IntegerField()

    def __str__(self):
        return self.url

class Warning(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE, related_name='warnings')
    created_at = models.DateTimeField(auto_now_add=True)
    result_code = models.IntegerField()