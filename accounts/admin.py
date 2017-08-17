from django.contrib import admin
from django.utils.translation import ugettext as _

from authtools.admin import UserAdmin as BaseUserAdmin

from .models import User
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ( 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'passport_number', 'balance', 'token')}),
        (_('Permissions'), {'fields': ('is_active', 'is_closed', 'is_staff', 'is_superuser', 'is_manager',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('balance', 'token',)

