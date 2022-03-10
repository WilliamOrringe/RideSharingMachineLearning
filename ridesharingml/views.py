from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def show_leaflet(request):
    return render(request, 'ridesharing/index.html')
