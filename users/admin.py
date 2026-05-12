from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import User


@admin.register(User)
class UserAdmin(ModelAdmin, BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ['email', 'name', 'role', 'is_active', 'is_staff', 'created_at']
    list_filter  = ['role', 'is_active', 'is_staff']
    search_fields = ['email', 'name']
    ordering = ['-created_at']
    list_per_page = 25

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Shaxsiy', {'fields': ('name', 'role')}),
        ('Huquqlar', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Sana', {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'password1', 'password2'),
        }),
    )
    readonly_fields = ['created_at', 'last_login']
