from django.contrib import admin
from django.urls import path, include
from .views import ListEvents, CreateEvent

urlpatterns = [
    path('api/list/', ListEvents, name="list_events"),
    path('api/create/', CreateEvent, name="create_event"),
]