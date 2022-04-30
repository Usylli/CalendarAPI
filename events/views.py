from datetime import timedelta
from email.policy import default
import json
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token

from accounts.models import Users
from .serializers import EventListSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListEvents(request):
    access_token = request.COOKIES['access_token']
    user_id = Token.objects.get(key=access_token).user_id
    user = Users.objects.get(id=user_id)
    events = user.event_set.all()
    serializer = EventListSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateEvent(request):
    data = {}
    reqBody = json.loads(request.body)
    access_token = request.COOKIES['access_token']
    user_id = Token.objects.get(key=access_token).user_id
    data['user'] = user_id
    data["message"] = "event created successfully"
    data["name"] = reqBody.get('name')
    data["start_date"] = reqBody.get('start_date', timezone.now())
    data["end_date"] = reqBody.get('end_date', timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999))
    data["ReminderTime"] = reqBody.get('reminder_time', timezone.now() + timedelta(hours=1))
    serializer = EventListSerializer(data=data)
    if serializer.is_valid():
        event = serializer.save()
        event.save()
        data["message"] = "event created successfully"
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = serializer.errors
        return Response(data)