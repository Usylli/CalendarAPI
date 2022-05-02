from django.contrib import admin
from django.urls import path, include
from .views import ListEvents, CreateEvent, addEventView, indexView, indexViewByMonth

app_name = 'events'

urlpatterns = [
    path('api/list/', ListEvents, name="list_events"),
    #path('api/list/month<int:num>', ListEvents, name="list_events_month"),
    path('api/create/', CreateEvent, name="create_event"),
    path('', indexView, name="index"),
    path('add', addEventView, name="add_event")
]