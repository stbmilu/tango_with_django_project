from django.urls import path
from rango import views

'''
this is the rango app urls file
'''

app_name = 'rango'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
]
