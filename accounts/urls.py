from django.urls import path
from .views import Register_Users, User_logout, login_user, login_u, register_u

app_name = 'users'
urlpatterns = [
   path('login', login_u, name="login"),
   path('register', register_u, name="register"),
   path('api/register_user/', Register_Users, name="register_api"),
   path('api/login_user/', login_user, name="login_api"),
   path('api/logout_user/', User_logout, name="logout_api")
]
