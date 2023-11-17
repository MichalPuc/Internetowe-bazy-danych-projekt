# views.py w silownia_app

from django.shortcuts import render
from .models import Client

def list_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients/list.html', {'clients': clients})
