from django.http import HttpResponse
from django.shortcuts import render
import requests
import socket
import http.server
import socketserver
from . import server


def validate(key):
    if 'https://' not in key:
        return {'error' : 'Invalid API', 'value' : 0}
    if 'api.thingspeak' not in key:
        return {'error' : 'Invalid API', 'value' : 0}
    if '.json' not in key:
        return {'error' : 'Invalid API', 'value' : 0}
    s = key.split('channels/')
    for i,j in enumerate(s[1]):
        if j.isnumeric():
            continue
        else:
            n = s[1][:i]
            break
    kk = s[1].split(n+'/fields/')
    chrt = 'https://thingspeak.com/channels/' + n + '/charts/' + kk[1][0] + '?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15'
    print(chrt)
    return {'error' : '', 'value' : 1, 'channel' : n, 'field' : kk[1][0], 'iframe' : chrt}

def data(request):
    # kk = server.readTemp()
    # Delete Below code
    PORT = 8000
    Temp = 0
    class MyTCPServer(socketserver.TCPServer):
        def server_bind(self):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print(self.server_address)
            self.socket.bind(self.server_address)

    Handler = http.server.ThreadingHTTPServer

    httpd = MyTCPServer(("", PORT), Handler)

    # os.chdir("/My/Webpages/Live/here.html")
    k = httpd.socket.listen(5)
    print(k)
    (clientsocket, address) = httpd.socket.accept()
    print(12)
    Temp = clientsocket.recv(1024)
    clientsocket.send(Temp)
    print(Temp)
    # httpd.serve_forever()
    # delete above Code

    if request.method == 'GET':
        context = {}
        return render(request, 'tempReader/urlPage.html', context)
        
    elif request.method == 'POST':
        api_key = request.POST.get('API_KEY') #https://api.thingspeak.com/channels/2014997/feeds.json?results=2
        is_validKey = validate(api_key)
        if is_validKey['value']:
            print(is_validKey['channel'], is_validKey['field'])
            try:
                response = requests.get(api_key).json()
                if response:
                    context = {'temperature' : response['feeds'][0]['field'+is_validKey['field']], 'ch_f_if' : is_validKey}
                    # return HttpResponse(context['temperature'])
                    return render(request, 'tempReader/tempDisplay.html', context)
                    #return HttpResponse("<h1>"+"Temperature is "+str(response['feeds'][0]['field1'])+"</h1>")
                else:
                    return HttpResponse("<h1>" + "This is not a valid API_KEY" + "</h1>")
            except:
                return HttpResponse("<h3>" + "This is not a valid API_KEY" + "</h3>")
            
        else:
            return HttpResponse("<h1>" + is_validKey['error'] + "</h1>")
        
def rw_data(request):
    context = {}
    return render(request, 'tempReader/options.html', context)

def wr_data(request):
    context = {}
    if request.method == 'GET':
        context = {'led_val' : 0, 'api_val' : ''}
        return render(request, 'tempReader/writeData.html', context)
    elif request.method == 'POST':
        wr_api = request.POST.get('write_api')
        context['api_val'] = wr_api
        led_val = request.POST.get('led_val')
        led_val = 0 if (str(led_val) == 'None') else 1
        context['led_val'] = led_val
        wr_api = str(wr_api) +'='+str(led_val)
        print(wr_api)
        resp = requests.post(wr_api)
        return render(request, 'tempReader/writeData.html', context)