from django.forms import ValidationError
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from psycopg2 import IntegrityError
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Users
from .serializers import RegistrationSerializer
import json

@api_view(["POST"])
@permission_classes([AllowAny])
def Register_Users(request):
    try:
        data = {}
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = True
            account.save()
            token = Token.objects.get_or_create(user=account)[0].key
            data["message"] = "user registered successfully"
            data["email"] = account.email_address
            data["username"] = account.username
            data["token"] = token
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED)
    except IntegrityError as e:
        account=Users.objects.get(username='')
        account.delete()
        raise ValidationError({"400": f'{str(e)}'})
    
    except KeyError as e:
        print(e)
        raise ValidationError({"400": f'Field {str(e)} missing'})
    
@api_view(["POST"])   
@permission_classes([AllowAny])
def login_user(request):
    data = {}
    reqBody = json.loads(request.body)
    email = reqBody['email_address']
    password = reqBody['password']
    try:
        account = Users.objects.get(email_address=email)
    except BaseException as e:
        raise ValidationError({"400": f'{str(e)}'}) 
    
    token = Token.objects.get_or_create(user=account)[0].key
    if not check_password(password, account.password):
        raise ValidationError({"message": "Incorrect Login Credentials"})
    
    if account:
        if account.is_active:
            login(request, account)
            data["message"] = "user logged in"
            data["email_address"] = account.email_address
            data["token"] = token
            response = Response(data)
            response.set_cookie('access_token', token)

            return response
        else:
            raise ValidationError({"404": f'Account not active'})
    else:
        raise ValidationError({"400": f'Account doesnt exist'})
            
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):
    access_token = request.COOKIES['access_token']
    if access_token:
        hed = {'Authorization': 'Token ' + access_token}
        response = Response('User Logged out successfully', headers=hed)
        response.delete_cookie('access_token')
        request.user.auth_token.delete()
        logout(request)
        return response
    else:
        return Response({"detail": "s credentials were not provided."})
    
    
    
    
    
    
    
#     {
# "email_address":"test@gmail.com",
# "username":"khabib",
# "password":"1234",
# "name":"bibib"
# }

