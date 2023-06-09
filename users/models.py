from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from datetime import date
from django.contrib.gis.db import models
from core.models import Project

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

    def get_user(self, email, password, **other_fields):
        try:
            user = self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        
        return None
    
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

class Address(models.Model):
    home_address = models.CharField(max_length = 150, null=True, blank=True,)
    location = models.PointField(null=True, blank=True, srid=4326)

    def __str__(self):
        return self.home_address

class User(AbstractBaseUser, PermissionsMixin, SoftDeleteModel): #use default permission facilities that Django has

    objects = CustomUserManager()
    all_objects = SoftDeleteManager()

    email = models.EmailField(_('email address'), unique = True)
    user_name = models.CharField(max_length = 150, unique = True)
    first_name = models.CharField(max_length = 150)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    last_name = models.CharField(max_length=250)
    contact = models.CharField(unique=True)
    date_joined = models.DateField(null=True)
    bio = models.TextField(blank=True)

    dob = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile/", blank=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True, related_name='users')

    website = models.URLField(blank=True)
    github = models.URLField(blank=True)

    is_staff = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name', 'contact']

    @property
    def age(self):
        if self.dob is not None:
            today = date.today()
            age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            return age
        return None


    def delete(self, using=None, keep_parents=False, hard=False):
        if hard:
            super().delete(using=using, keep_parents=keep_parents)
        else:
            self.soft_delete()
            
    class Meta:
        db_table = "user"

    def __str__(self):
        return f"{self.email} ({self.pk})"
