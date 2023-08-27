from django.contrib import admin
from .models import Chat, Group
# Register your models here.

class ChatAdmin(admin.ModelAdmin):
    list_display = ['content', 'timestamp', 'group']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Chat, ChatAdmin)
admin.site.register(Group, GroupAdmin)