from django.http import HttpResponse
from django.shortcuts import render
import requests
# from .. import server11

def data(request):
    response = requests.get('https://api.thingspeak.com/channels/2014997/feeds.json?results=2').json()
    if response:
        return HttpResponse("<h1>"+"Temperature is "+str(response['feeds'][0]['field1'])+"</h1>")
    else:
        return HttpResponse("<h1>DND</h1>")