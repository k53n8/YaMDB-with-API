from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
