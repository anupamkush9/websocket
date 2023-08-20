from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        # Your logic for handling the GET request
        return render(request, 'websocket_app/index.html',)
    
