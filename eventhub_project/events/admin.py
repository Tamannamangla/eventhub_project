from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,EventManager

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'name', 'phone', 'gender', 'dob', 'is_staff', 'is_superuser')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone', 'gender', 'dob', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'gender', 'dob', 'address', 'password1', 'password2'),
        }),
    )

class EventManagerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'password',
                    'gender', 'hobbies', 'address', 'created_at']
    list_filter = ['gender', 'created_at']

admin.site.register(EventManager, EventManagerAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
