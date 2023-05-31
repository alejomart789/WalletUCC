from django.urls import path
from . import views

app_name = 'mainApp'


urlpatterns = [
    path('', views.index, name='inicio'),
]