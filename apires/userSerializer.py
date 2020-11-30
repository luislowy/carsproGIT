
#user serializer

#django
from django.contrib.auth import authenticate
from django.utils.timezone import now

#res_framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from appcar.models import Notificacion, Carro

class UserHistorySerializer(serializers.ModelSerializer):
	plac=serializers.SerializerMethodField('nose')
	def nose (self, data):
		Q=Carro.objects.get(idalarma=data.device)
		return Q.placa
	class Meta:
		model = Notificacion
		fields = (
			'user_relacion',
			'notif', 
			'latitud', 
			'longitud', 
			'fecha', 
			'plac' ## agregar un nuevo campo al json 
		)	
	


class UserModelSerializer(serializers.ModelSerializer):

	class Meta:
		model=User
		fields=(
			'username',
			'first_name',
			'last_name',
			'email'
			)

class UserLoginSerializer(serializers.Serializer):
	email=serializers.CharField()
	password=serializers.CharField(min_length=8, max_length=64)
	def validate(self, data):
		user=authenticate(username=data['email'], password=data['password'])
		if not user:
			raise serializers.ValidationError("credenciales invalidas")
		self.context['user']=user	
		return data	

	def create(self, data):
		#obtiene o crea un token
		token, created=Token.objects.get_or_create(user=self.context['user'])
		return self.context['user'], token.key