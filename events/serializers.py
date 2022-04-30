from rest_framework import serializers
from .models import Event

class EventListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ("user", "name", "start_date", "end_date", "ReminderTime")
        