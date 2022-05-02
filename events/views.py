from ast import Not
from audioop import reverse
from datetime import timedelta, datetime
from email.policy import default
import json
from django.urls import reverse_lazy
import requests
from requests.structures import CaseInsensitiveDict
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from accounts.models import Users
from .serializers import EventListSerializer
import time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListEvents(request):
    access_token = request.headers['Authorization'][6:]
    user_id = Token.objects.get(key=access_token).user_id
    user = Users.objects.get(id=user_id)
    month = request.GET.get('month', None)
    if month is None:
        events = user.event_set.order_by('start_date')
    else:
        events = user.event_set.filter(start_date__month = month)
    
    serializer = EventListSerializer(events, many=True) 
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateEvent(request):
    data = {}
    reqBody = json.loads(request.body)
    access_token = request.headers['Authorization'][6:]
    user_id = Token.objects.get(key=access_token).user_id
    user = Users.objects.get(pk=user_id)
    data['user'] = user_id
    data["message"] = "event created successfully"
    data["name"] = reqBody.get('name')
    data["start_date"] = reqBody.get('start_date', timezone.now())
    data["end_date"] = reqBody.get('end_date', timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999))
    data["ReminderTime"] = reqBody.get('reminder_time')
    serializer = EventListSerializer(data=data)
    if serializer.is_valid():
        event = serializer.save()
        event.save()
        data["message"] = "event created successfully"
        mail(event.name, user.email_address, event.ReminderTime)
        
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = serializer.errors
        return Response(data)
    
def indexView(request):
    month_num = request.GET.get('month', None)
    month_add = '' if month_num is None else f'?month={month_num}'
    url = request.scheme + '://' + request.META['HTTP_HOST'] + reverse_lazy('events:list_events') + month_add
    access_token = request.COOKIES.get('access_token', None)
    if access_token is None:
        return render(request, 'restricted.html')
    else:
        headers = CaseInsensitiveDict()
        headers["Authorization"] = "token " + access_token

        resp = requests.get(url, headers=headers)
        content = resp.content.decode("utf-8")
        events = json.loads(content)
        print(events)
        return render(request, 'index.html', {"events" : events})

def indexViewByMonth(request, num=1):
    url = request.scheme + '://' + request.META['HTTP_HOST'] + reverse_lazy('events:list_events')
    access_token = request.COOKIES.get('access_token', None)
    if access_token is None:
        return render(request, 'restricted.html')
    else:
        headers = CaseInsensitiveDict()
        headers["Authorization"] = "token " + access_token
        
        resp = requests.get(url, headers=headers)
        content = resp.content.decode("utf-8")
        events = json.loads(content)
        print(events)
        return render(request, 'index.html', {"events" : events})
    
def addEventView(request):
    return render(request, 'addEvent.html')
    
def mail(event_name, user_address, send_time):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('alihangames1@gmail.com', 'UzumakiAlikhan')
    msg = message(event_name)
    to = [user_address]
    send_time = datetime.fromisoformat(send_time.isoformat())
    time.sleep(send_time.timestamp() - time.time())
    smtp.sendmail(from_addr="alihangames1@gmail.com",
                to_addrs=to, msg=msg.as_string())
    smtp.quit()

def message(text=""):
	msg = MIMEMultipart()
	msg['Subject'] = "Calendar Notification"
	msg.attach(MIMEText(text))

	return msg

