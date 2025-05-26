from django.contrib import admin
from userauth.models import User
# from import_export.admin import




class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


admin.site.register(User, UserAdmin)