from django import forms
from .models import *
from django.contrib.auth.models import User


class agregar_persona_form(forms.ModelForm):
	class Meta:
		model=Persona
		fields='__all__'

class agregar_carro_form(forms.ModelForm):
	class Meta:
		model=Carro
		fields='__all__'

class confirmar_user_form(forms.Form):
	identificacion=forms.CharField(widget= forms.TextInput(attrs={'tipe': 'number','placeholder':'Identificacion'}))
	respuesta=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Respuesta'}))

	def clean_respuesta(self):
		
		respuesta=self.cleaned_data['respuesta']
		identificacion=self.cleaned_data['identificacion']
		if Persona.objects.filter(identificacion=identificacion).exists():
			ide=Persona.objects.get(identificacion=identificacion)
			if ide.respuesta== respuesta:
				pass
			else:
				raise forms.ValidationError('respuesta erronea')
			if ide.usuario:
				raise forms.ValidationError('ya tiene usuario creado')
			else:
				pass
		else:
			raise forms.ValidationError('no se encuentra registrado')


class login_form(forms.Form):
	
	usuario = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre user'}))
	clave = forms.CharField(widget= forms.PasswordInput(render_value=False, attrs={'class':'form-control', 'placeholder':'Contraseña'}))
	

class register_form(forms.Form):
	username = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Nombre user'}))
	email = forms.EmailField(widget = forms.TextInput(attrs={'placeholder':'Email'}))
	password1 = forms.CharField(label = 'Password', widget=forms.PasswordInput(render_value=False, attrs={'placeholder':'Contraseña'}))
	password2 = forms.CharField(label = 'Confirmar Password', widget=forms.PasswordInput(render_value=False, attrs={'placeholder':'Contraseña'}))
	


	def clean_username(self):
		username=self.cleaned_data['username']
		try:
			u=User.objects.get(username=username)
		except  User.DoesNotExist:
			return username
		raise forms.ValidationError('Nombre de user ya existe')

	def clean_email(self):

		email=self.cleaned_data['email']
		try:
			email=User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('email ya existe')

	def clean_password2(self):
		password1=self.cleaned_data['password1']
		password2=self.cleaned_data['password2']
		if password1==password2:
			pass
		else:
			raise forms.ValidationError('Password no coinciden')

class contacto_form(forms.ModelForm):   # se utiliza forms.ModelForm cuando se quiere trabajar con el formulario del diseño
	class Meta:                         #de los modelos de la ase de datos
		model=Contacto
		fields='__all__'
	
class dispositivos_form(forms.Form):
	idalarma = forms.CharField(widget = forms.TextInput())

class notificacion_form(forms.ModelForm):
	class Meta:
		model=Notificacion
		fields='__all__'




	



