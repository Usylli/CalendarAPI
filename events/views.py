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
    events = user.event_set.all()
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

    # initialize connection to our email server,
    # we will use gmail here
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()

    # Login with your email and password
    smtp.login('alihangames1@gmail.com', 'UzumakiAlikhan')

    # Call the message function
    msg = message(event_name)

    # Make a list of emails, where you wanna send mail
    to = [user_address]
    
    send_time = datetime.fromisoformat(send_time.isoformat())
    time.sleep(send_time.timestamp() - time.time())

    smtp.sendmail(from_addr="alihangames1@gmail.com",
                to_addrs=to, msg=msg.as_string())

    # Finally, don't forget to close the connection
    smtp.quit()

def message(text=""):
	
	# build message contents
	msg = MIMEMultipart()
	
	# Add Subject
	msg['Subject'] = "Calendar Notification"
	
	# Add text contents
	msg.attach(MIMEText(text))

	return msg

