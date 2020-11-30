
# view user

# modelos de appcar
from appcar.models import Notificacion, Carro

#Django reframework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
#Django
from django.utils.timezone import now
#serializer
from .userSerializer import (
	UserLoginSerializer,
	UserModelSerializer,
	UserHistorySerializer)


class vista_historia_API(APIView):

	def get(self, request, *args, **kwargs):
		queryset=Notificacion.objects.filter(user_relacion=request.user)
		serializer = UserHistorySerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	

class vista_login_API(APIView):
	permission_classes = []
	def post(self, request, *args, **kwargs):
		serializer=UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user, token=serializer.save()
		data={
			'user':UserModelSerializer(user).data,
			'access_token':token
		}
		return Response(data, status=status.HTTP_201_CREATED)

