from django.contrib import admin
from django.urls import path
from tempReader.views import data, wr_data, rw_data

urlpatterns = [
    path('', rw_data, name='rw_data'), #root path :)

    path('rd_data/', data, name="read_data"), # read data from api 
    path('wr_data/', wr_data, name = 'write_data'), # write data to api
]