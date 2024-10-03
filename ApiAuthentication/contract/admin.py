from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    list_display = ('Email', 'Name', 'Gender', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'Gender')
    
    # The fieldsets to organize the form in the admin.
    fieldsets = (
        (None, {'fields': ('Email', 'password')}),
        ('Personal info', {'fields': ('Name', 'Gender')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )

    # Fields to be displayed on the "add user" form in the admin panel.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('Email', 'Name', 'Gender', 'password1', 'password2'),
        }),
    )

    search_fields = ('Email', 'Name')
    ordering = ('Email',)
    filter_horizontal = ()

# Register the new UserAdmin
admin.site.register(User, UserAdmin)
