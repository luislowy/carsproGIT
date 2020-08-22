from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.views import(TokenObtainPairView, TokenRefreshView,)
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

urlpatterns=[
path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
path('agregar_persona/', login_required (vista_agregar_persona), name= 'vista_agregar_persona'),
path('agregar_carro/', vista_agregar_carro, name= 'vista_agregar_carro'),
path('confirmar_user/', vista_confirmar_user, name='vista_confirmar_user'),
path('mensaje/', vista_mensaje, name= 'vista_mensaje'),
path('accounts/login/', vista_login, name='vista_login'),
path('logout/', vista_logout, name='vista_logout'),
path('register/<str:iden>/', vista_register, name='vista_register'),
path('inicio/', vista_inicio, name='vista_inicio'),
path('lista_persona/', vista_lista_persona, name='vista_lista_persona'),
path('lista_carro/', vista_lista_carro, name='vista_lista_carro'),
path('lista_token/', vista_lista_token, name='vista_lista_token'),
path('contacto/', vista_contacto, name='vista_contacto'),
path('eliminar_persona/<int:id_Persona>/', vista_eliminar_persona, name= 'vista_eliminar_persona'),
path('eliminar_carro/<int:id_Carro>/', vista_eliminar_carro, name= 'vista_eliminar_carro'),
path('notificacion/',  vista_notificacion, name='vista_notificacion'),
path('inicio_superuser/',login_required (vista_inicio_superuser), name='inicio_superuser'),
path('tokenRfirebase/', tokenRfirebase, name='tokenRfirebase'),
path('resibir_info_controlador/',resibir_info_controlador, name='resibir_info_controlador'),
path('liberar/token/', liberar_token, name='liberar_token'),
path('solodata/', solodata, name='solodata')

]
