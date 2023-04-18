from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from users.models import UserProfile
from django.utils.timezone import now

# Register your models here.
class UserAdminConfig(UserAdmin):

    search_fields = ('email', 'user_name', 'first_name',)
    filter = ('email', 'user_name', 'first_name', 'address', 'is_active', 'is_staff', 'is_deleted')
    ordering = ('-date_joined',)
    list_display = ('email', 'user_name', 'first_name', 'last_name', 'contact', 'address', 'is_active', 'is_staff', 'is_deleted')
   
    # To eliminate field error
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name', 'contact', 'address',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
        ('Personal', {'fields': ('about',)}),
        ('Soft Delete', {'fields': ('is_deleted', 'deleted_at',)}),
    )

    formfield_overrides = {
        User.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name', 'contact', 'address', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )

    def delete_queryset(self, request, queryset):
        queryset.update(deleted_at=now())

admin.site.register(User, UserAdminConfig)

class UserProfileAdminConfig(admin.ModelAdmin):
    filter = ('user', 'display_age',)
    list_display = ('user', 'dob', 'age', 'address', 'bio', 'github', 'website')

    # To eliminate field error
    fieldsets = (
        ('User', {'fields': ('user', 'dob', 'address', 'bio',)}),
        ('Profile', {'fields': ('profile_image',)}),
        ('Social', {'fields': ('github', 'website',)}),
    )

    formfield_overrides = {
        User.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'dob', 'address', 'bio' 'github', 'website', 'profile_image',)
        }),
    )
admin.site.register(UserProfile, UserProfileAdminConfig)