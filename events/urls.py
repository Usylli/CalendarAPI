from django.contrib import admin
from django.urls import path, include
from .views import ListEvents, CreateEvent

urlpatterns = [
    path('list/', ListEvents, name="list_events"),
    path('create/', CreateEvent, name="create_event"),
]