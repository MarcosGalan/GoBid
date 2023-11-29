from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'dni', 'age', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'dni', 'age')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'dni', 'age', 'is_staff', 'is_superuser')}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin, app_label='auth')
