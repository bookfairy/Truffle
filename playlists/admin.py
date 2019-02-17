from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')    
    
admin.site.register(Photo)
admin.site.register(Card)
admin.site.register(Tag)
admin.site.register(Comments)
