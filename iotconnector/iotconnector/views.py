from django.http import HttpResponse
from django.shortcuts import render
import requests

def mainPage(request):
    context = {}
    return render(request, 'main.html', context)