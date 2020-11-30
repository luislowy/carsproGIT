#import de Django
from django.urls import path

#view
from .userView import *

urlpatterns = [
    path('user/login/', vista_login_API.as_view(), name="login"),
    path('user/historia/', vista_historia_API.as_view(), name="historia"),
  
]
