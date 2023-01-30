from django.http import HttpResponse
from django.shortcuts import render
import requests

def validate(key):
    if 'https://' not in key:
        return {'error' : 'Make sure to Include "https://" prefixed to your URL', 'value' : 0}
    if 'api.thingspeak' not in key:
        return {'error' : 'Please provide API KEY from ThingSpeak', 'value' : 0}
    if '.json' not in key:
        return {'error' : 'Provided Link Does not Exist or Could\'nt parsed to be a JSON String', 'value' : 0}
    return {'error' : '', 'value' : 1}

def data(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'tempReader/urlPage.html', context)
        
    elif request.method == 'POST':
        api_key = request.POST.get('API_KEY')
        is_validKey = validate(api_key)
        if is_validKey['value']:
            try:
                response = requests.get(api_key).json()
                if response:
                    return HttpResponse("<h1>"+"Temperature is "+str(response['feeds'][0]['field1'])+"</h1>")
                else:
                    return HttpResponse("<h1>" + "This is not a valid API_KEY" + "</h1>")
            except:
                return HttpResponse("<h1>" + "This is not a valid API_KEY" + "</h1>")
            
        else:
            return HttpResponse("<h1>" + is_validKey['error'] + "</h1>")