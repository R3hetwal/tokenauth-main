from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from django.utils.timezone import now

# Register your models here.
class UserAdminConfig(UserAdmin):

    search_fields = ('email', 'user_name', 'first_name',)
    filter = ('email', 'user_name', 'first_name', 'address', 'is_active', 'is_staff',)
    ordering = ('-date_joined',)
    list_display = ('email', 'user_name', 'first_name', 'last_name', 'dob', 'contact', 'address', 'is_active', 'is_staff', )
   
    # To eliminate field error
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name',)}),
        ('Personal', {'fields': ('contact', 'address', 'dob',)}),
        ('Profile', {'fields': ('bio', 'profile_image',)}),
        ('Social', {'fields': ('github', 'website',)}),
        ('Soft Delete', {'fields': ('is_active', 'deleted_at',)}),
        ('Permissions', {'fields': ('is_staff',)}),
    )

    formfield_overrides = {
        User.bio: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
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
