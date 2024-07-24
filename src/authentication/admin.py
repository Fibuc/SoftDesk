from django.contrib import admin
from authentication.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined', 'can_be_contacted', 'can_data_be_shared')

admin.site.register(User, UserAdmin)