from django.contrib import admin
from .models import Profile
# Register your models here.

@admin.register(Profile)
class ProfielAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_name', 'get_email')    
    
    
    def get_email(self, obj):
        return obj.user.email
    
    get_email.short_description = '이메일'
    
    def get_name(self, obj):
        return obj.user.last_name+obj.user.first_name
    
    get_name.short_description = '이름'