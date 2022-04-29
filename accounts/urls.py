from django.urls import path
from .views import Register_Users, User_logout, login_user

app_name = 'users'
urlpatterns = [
   path('create/', Register_Users, name="create"),
   path('login_user/', login_user, name="login"),
   path('logout_user/', User_logout, name="logout")
]
