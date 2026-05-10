from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('Role', {
            'fields': ('role',)
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'role')
        }),
    )

    list_display = ('username', 'email', 'role', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)