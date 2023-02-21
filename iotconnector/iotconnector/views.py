from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import csv
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def mainPage(request):
    context = {}
    print(request.method)
    if request.method == 'GET':
        info = list(request.GET.items())
    if request.method == 'POST':
        info = list(request.POST.items())
    print(info)
    if(len(info)):
        with open('data.csv', 'a') as f:
            # print(info[0])
            f.write(info[0][0]+','+str(info[0][1]))
            f.write('\n')
        f.close()
    with open('data.csv', 'r') as f:
        data = csv.reader(f)
        totals = [row  for row in data]
        if len(totals):
            labels = [row[0] for row in totals]
            values = [row[1] for row in totals]
        else:
            labels = []
            values = []
    f.close()
    ret_data = {'Reply' : 'Hey ! We are connected !!'}
    context['labels'] = labels
    context['values'] = values
    return JsonResponse(ret_data, status = 201) #and HttpResponse('<h1>Status : 200</h1>')
    # return JsonResponse(ret_data, status = 201) and render(request, 'main.html', context)
    # return render(request, 'main.html', context)