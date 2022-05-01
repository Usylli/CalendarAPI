from django.contrib import admin
from django.urls import path, include
from .views import ListEvents, CreateEvent, addEventView, indexView

app_name = 'events'

urlpatterns = [
    path('api/list/', ListEvents, name="list_events"),
    path('api/create/', CreateEvent, name="create_event"),
    path('', indexView, name="index"),
    path('add', addEventView, name="add_event")
]