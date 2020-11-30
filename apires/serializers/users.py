from django.contrib.auth import authenticate

from res_framework import serializers


class UserLoginSerializer(serializers.Serializer):
	email=serializers.EmailField()
	password=serializers.CharField(min_length=8, max_length=64)
	def validate(self, data):
		user=authenticate(username=data['email'], password=data['password'])
		if not user:
			raise serializers.ValidationError("credenciales invalidas")
		return data	

