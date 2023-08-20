from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        # Your logic for handling the GET request
        return render(request, 'websocket_app/index.html',)
    

class RoomView(View):
    template_name = 'websocket_app/room.html'  # Replace with your template path

    def get(self, request, room_name):
        context = {"room_name": room_name}
        return render(request, self.template_name, context)
