from django.contrib import admin
from users.models import Address, User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from django.utils.timezone import now
from django.utils.translation import gettext as _

# Register your models here.
class UserAdminConfig(UserAdmin):

    search_fields = ('email', 'user_name', 'first_name',)
    filter = ('email', 'user_name', 'first_name', 'address', 'is_active', 'is_staff',)
    ordering = ('-date_joined',)
    list_display = ('email', 'user_name', 'first_name', 'last_name', 'project', 'dob', 'contact', 'address', 'is_active', 'is_staff', )
    actions = ['delete_selected']
    
    def delete_selected(self, request, queryset):
        queryset.delete(hard=True)
    #This allows the same action to be used for different models and have the description automatically 
    # adjusted to match the model being acted upon.
    delete_selected.short_description = _("Delete selected %(verbose_name_plural)s")

    def delete_queryset(self, request, queryset):
        queryset.delete(hard=True)

    # To eliminate field error
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name',)}),
        ('Task', {'fields': ('project',)}), 
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
    
    def delete_selected(self, request, queryset):
        queryset.delete()

admin.site.register(User, UserAdminConfig)
admin.site.register(Address)