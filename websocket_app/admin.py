from django.contrib import admin
from .models import Chat, Group, Ticket
# Register your models here.

class ChatAdmin(admin.ModelAdmin):
    list_display = ['content', 'timestamp', 'group']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']

class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']


admin.site.register(Chat, ChatAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Ticket, TicketAdmin)
