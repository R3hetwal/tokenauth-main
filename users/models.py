from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from datetime import date

# Create your models here.
class CustomUserManager(BaseUserManager):

    
    def create_user(self, email, user_name, first_name, password, **other_fields):

        # Validating email
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff = True.'
            )

        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser = True.'
            )

        return self.create_user(email, user_name, first_name, password, **other_fields)

class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True, is_active=False)

class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, SoftDeleteModel): #use default permission facilities that Django has

    objects = CustomUserManager()
    all_objects = SoftDeleteManager()

    email = models.EmailField(_('email address'), unique = True)
    user_name = models.CharField(max_length = 150, unique = True)
    first_name = models.CharField(max_length = 150) 
    last_name = models.CharField(max_length=250)
    contact = models.BigIntegerField(unique=True)
    address = models.CharField(max_length=250)
    date_joined = models.DateField(null=True)
    about = models.TextField(_('about'), max_length = 500, blank = True)

    is_staff = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name', 'contact']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    location = models.CharField(max_length=50, blank=True)

    address = models.CharField(max_length=50, blank=True)

    dob = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile/", blank=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True) 

    @property
    def age(self):
        if self.dob is not None:
            today = date.today()
            age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            return age
        return None

    def __str__(self):
        return f"{self.user.user_name}'s profile"
    

