from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from websocket_app.models import Group, Chat 

# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        # Your logic for handling the GET request
        return render(request, 'websocket_app/index.html',)
    

class RoomView(View):
    template_name = 'websocket_app/room.html'  # Replace with your template path

    def get(self, request, room_name):
        group = Group.objects.filter(name=room_name).first()
        chats = []
        if group:
            chats = Chat.objects.filter(group__name = room_name)
        else:
            Group.objects.create(name=room_name)

        return render(request, self.template_name, {'chats':chats, "room_name": room_name})
