from django.contrib import admin
from .models import CrimeReport
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class CrimeReportAdmin(admin.ModelAdmin):
    list_display = ('year','date','month','longitude','latitude','day_of_week')
    list_filter = ('year','date','month','longitude','latitude','day_of_week')
    search_fields = ('year','date','month','longitude','latitude','day_of_week')
    ordering = ('-year',)

# Register the CrimeReport model with the CrimeReportAdmin class
admin.site.register(CrimeReport, CrimeReportAdmin)

# Customizing the User model in the admin
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
