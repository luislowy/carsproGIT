from django.db import models
from django.contrib.auth.models import User


class Persona(models.Model):
	nombre=models.CharField(max_length=100)
	apellido=models.CharField(max_length=100)
	identificacion=models.DecimalField(max_digits=12, decimal_places=0)
	telefono=models.DecimalField(max_digits=12, decimal_places=0)
	direccion=models.CharField(max_length=100)
	preguntasegu=models.CharField(max_length=100)
	respuesta=models.CharField(max_length=50)
	usuario=models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		return str(self.identificacion)

class Carro(models.Model):
	modelo=models.CharField(max_length=15)
	ciudad=models.CharField(max_length=30)
	marca=models.CharField(max_length=100)
	placa=models.CharField(max_length=10, unique=True)
	idalarma=models.CharField(max_length=20, unique=True)
	persona=models.ForeignKey(Persona, on_delete=models.CASCADE)
	def __str__(self):
		return self.placa

class Contacto(models.Model):
	opciones=(('bb','ballenas jorbadas'),('ba', 'ballenas de lo frio'), ('ga', 'gallina'), ('sa','sapo'),)
	nombres=models.CharField(max_length=100)
	apellidos=models.CharField(max_length=100)
	telefono=models.DecimalField(max_digits=12, decimal_places=0)
	email=models.EmailField(max_length=200)
	asunto=models.CharField(max_length=2, choices=opciones)
	mensaje=models.CharField(max_length=200)
	def __str__(self):
		return str(self.identificacion)

class Notificacion(models.Model):
	notif=models.CharField(max_length=100)
	posicion=models.DecimalField(max_digits=30, decimal_places=12)
	idala=models.CharField(max_length=20)

class Tokenfirebase(models.Model):
	token=models.CharField(max_length=500)
	usuario=models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.username;
		


