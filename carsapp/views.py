from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
#from django.shortcuts import render_to_response
import firebase_admin
from firebase_admin import credentials, auth, firestore, messaging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests
import datetime


# Create your views here.
#@login_required

def vista_agregar_persona(request):
	if request.method=='POST':
		formulario=agregar_persona_form(request.POST, request.FILES)
		if formulario.is_valid():
			pers=formulario.save(commit=False)
			pers.save()
			formulario.save_m2m()
			
			return redirect('/agregar_carro/')
	else:
		formulario=agregar_persona_form()
	return render(request,'agregar_persona.html', locals())

def vista_agregar_carro(request):
	if request.method=='POST':
		formulario=agregar_carro_form(request.POST, request.FILES)
		if formulario.is_valid():
			car=formulario.save(commit=False)
			car.save()
			return redirect('/mensaje/')
	else:
		formulario=agregar_carro_form()
	return render(request,'agregar_carro.html', locals())

def vista_mensaje(request):
	return render(request,'mensaje.html')

def vista_confirmar_user(request):
	identificacion= ""
	respuesta= ""
	# capturo el id de la tabla usuario
	#for e in User.objects.all():
	#	print(e.id, e.username)
#para luego ver si ya tiene un usuario
	if request.method== 'POST':
		formulario=confirmar_user_form(request.POST)
		if formulario.is_valid():
			iden= formulario.cleaned_data['identificacion']
			return redirect('/register/'+iden)
	else:
		formulario=confirmar_user_form()
	return render(request, 'confirmar_user.html', locals())


def vista_login(request):
	usu=""
	cla=""
	ban =False
	if request.method== 'POST':
		formulario= login_form(request.POST)
		if formulario.is_valid():
			usu= formulario.cleaned_data['usuario']
			cla= formulario.cleaned_data['clave']
			usuario= authenticate(username=usu, password=cla)
			if usuario is not None and usuario.is_active:
				#e=User.objects.all()
				if usuario.is_superuser==1:
					login(request, usuario)
					return redirect('/inicio_superuser/')
				else:
					login(request, usuario)
					return redirect('/notificacion/')#direciono ala pag de las notificaciones 
			else:
				ban = True
				msj= "usuario o clave incorrecta"
				
	formulario= login_form()
	return render(request, 'login.html',locals())

def vista_logout(request):
	logout(request)
	return redirect('/inicio/')

'''def confirmar_user(request):
	formulario=confirmar_user_form()
	if request.method=='POST':
		formulario=confirmar_user_form(request.POST)
		if formulario.is_valid():
			return redirect('/register/')
	return render(request, 'confirmar_user.html', locals())'''



def vista_register(request,iden):
	formulario=register_form()
	if request.method=='POST':
		formulario=register_form(request.POST)
		if formulario.is_valid():
			usuario=formulario.cleaned_data['username']
			correo=formulario.cleaned_data['email']
			password1=formulario.cleaned_data['password1']
			password2=formulario.cleaned_data['password2']
			u=User.objects.create_user(username=usuario, email=correo, password=password1)
			u.save()
			idu=u.id
			#print('cscscsccsccscscs', idu)
	#----------------------------------------------------------------------------
			#no=Persona.objects.filter(identificacion=iden)
			#print('identificacion', no)
			Persona.objects.filter(identificacion=iden).update(usuario=idu)

			return redirect('/thanks_for_register/')
		else:
			return render(request,'register.html',locals())
	return render(request,'register.html',locals())

def vista_inicio(request):
	return render(request, 'inicio.html')

def vista_inicio_superuser(request):
	return render(request,'inicio_superuser.html')

def vista_lista_persona(request):
	lista=Persona.objects.filter()
	return render (request, 'lista_persona.html', locals())

def vista_lista_carro(request):
	lista=Carro.objects.filter()
	return render (request, 'lista_carro.html', locals())

def vista_eliminar_persona(request, id_Persona): # id_Persona se envia desde las url
	per=Persona.objects.get( id= id_Persona)
	per.delete()
	return redirect("/lista_persona/")

def vista_eliminar_carro(request, id_Carro): # id_Persona se envia desde las url
	pe=Carro.objects.get( id= id_Carro)
	pe.delete()
	return redirect("/lista_carro/")

def vista_lista_token(request):
	listatoken=Tokenfirebase.objects.filter()
	return render (request, 'lista_token.html', locals())	

def vista_contacto(request):

	if request.method=='POST':
		formulario=contacto_form(request.POST)# request.FILES  enviar archivos ima musci videos
		if formulario.is_valid():
			contc=formulario.save(commit=False)
			contc.save()
			#formulario.save_m2m() #para guardar cuando las tablas tienen relación de muchos a muchos 
			return redirect('/contacto/')
	else:
		formulario=contacto_form()
	return render(request,'contacto.html', locals())

# inicio para el registro del token del dispositivo
@csrf_exempt	
def tokenRfirebase(request):
	if request.method=='POST':
		tokenfires=request.POST.get('token')
		usee=request.POST.get('username')
		print('token de registro: ', tokenfires)
		print('--------------',usee)
		idd=User.objects.get(username=usee)
		print('++++++++', idd.id)
		pe=Tokenfirebase.objects.filter(token=tokenfires).exists()
		if pe==True:
			print("existe token")
		else:
			c=Tokenfirebase.objects.filter(usuario=idd.id).exists()
			if c==False:
				print("se puede registrar")
				Tokenfirebase.objects.create(token=tokenfires, usuario=idd)
			else:
				print("actualizar token")
				re=Tokenfirebase.objects.filter(usuario=idd.id)
				re.update(token=tokenfires)
							
	return HttpResponse('ok')
# fin para el registro del token del dispositivo
#------------------funcion para saber a que usuario enviar la notificacion---------------
@csrf_exempt
def resibir_info_controlador(request):

	if request.method=='POST':
		idalar=request.POST.get('serie')
		notu=request.POST.get('noty')

		if idalar is not None and notu is not None and notu!='movimiento':
			ca=Carro.objects.get(idalarma=idalar)
			print(ca.persona.usuario.id)
			to=Tokenfirebase.objects.get(usuario=ca.persona.usuario.id)
			tokenre=to.token
			posi=None
			print(tokenre)
			print(notu)
			envio_notificacionsingps(tokenre, notu)
			'''	userr=User.objects.get(relacion=ca.id)
			tokefir=Tokenfirebase.objects.get(relacion=userr.id)'''
		elif idalar is not None and notu is not None and notu=='movimiento':
			gp=request.POST.get('gps')
			ca=Carro.objects.get(idalarma=idalar)
			print(ca.persona.usuario.id)
			to=Tokenfirebase.objects.get(usuario=ca.persona.usuario.id)
			tokenre=to.token
			print(tokenre)
			print(notu)
			print(gp)
			envio_notificacion(tokenre, notu, gp)
		

			

	else:
		print("sapo")
	return HttpResponse('es nulo')


#------------------funcion para saber a que usuario enviar la notificacion---------------
@csrf_exempt
def solodata(request):
	if request.method=='POST':
		idalar=request.POST.get('serie')
		notu=request.POST.get('noty')

		if notu=='movimiento':
			ca=Carro.objects.get(idalarma=idalar)
			print(ca.persona.usuario.id)
			to=Tokenfirebase.objects.get(usuario=ca.persona.usuario.id)
			tokenre=to.token
			movo=request.POST.get('gps')
			print(tokenre)
			print(notu)
			envio_data(tokenre, notu, movo)

def envio_data(tokenre, notu, movo):
	if not firebase_admin._apps:
		cred = credentials.Certificate("static/carsafa-uni-firebase-adminsdk-ut950-f4f7d12592.json")
		firebase_admin.initialize_app(cred)
		if movo is not None:
			indice = movo.find(',')
			latitud = movo[:indice]
			longitud = movo[indice +1:]
			datas={
				'serie':idalar,
				'tiponoti':notu, 
				'latitud':latitud, 
				'longitud':longitud
			}
	message = messaging.Message(
		data=datas,
		token=tokenre,
	)			
	response = messaging.send(message)
	print('Successfully sent message:', response)
		


# -----------------------inicio para envio de notificacion----------------------------------
def envio_notificacion(tokenre, notu, posicion):
	if not firebase_admin._apps:
		cred = credentials.Certificate("C:/Users/USUARIO/Desktop/TRABAJOpts/carros/carsafa-uni-firebase-adminsdk-ut950-f4f7d12592.json")
		firebase_admin.initialize_app(cred)

	if posicion is not None:
		indice = posicion.find(',')
		latitud = posicion[:indice]
		longitud = posicion[indice +1:]
		print('latitud ' + latitud + ' longitud '+longitud)
	
	# See documentation on defining a message payload.
	message = messaging.Message(
		data={'lad':latitud, 'long':longitud},
		
		notification=messaging.Notification('MI CARRO', notu),
		android=messaging.AndroidConfig(
		#ttl=datetime.timedelta(seconds=3600),
        priority='high', 
        notification=messaging.AndroidNotification(
            icon='notify2',
            color='#F50D1E',
            sound='default_sound',
        
    	),
      
    	),

        #token=registro,
        token=tokenre,
	)


	response = messaging.send(message)
	print('Successfully sent message:', response)
	return HttpResponse('ok')

def envio_notificacionsingps(tokenre, notu):
	if not firebase_admin._apps:
		cred = credentials.Certificate("C:/Users/USUARIO/Desktop/TRABAJOpts/carros/carsafa-uni-firebase-adminsdk-ut950-f4f7d12592.json")
		firebase_admin.initialize_app(cred)

	# See documentation on defining a message payload.
	message = messaging.Message(
			
		notification=messaging.Notification('MI CARROsin gps', notu),
		android=messaging.AndroidConfig(
		#ttl=datetime.timedelta(seconds=3600),
        priority='high',
        notification=messaging.AndroidNotification(
            icon='notify1',
            color='#B99F38',
            sound='default_sound'
        	),
        
    	),

        #token=registro,
        token=tokenre,
	)


	response = messaging.send(message)
	print('Successfully sent message:', response)
	return HttpResponse('ok')


	
@csrf_exempt
def solodataTEM(request):
	server_key = 'AAAAhi_wSHU:APA91bH867I6QndLUr5RC6ZV5aIj720f4vRIak_l_zMde6vYdEDBicCbeeOzVWp6PBppAbAQAHBSu4ZfNIquSVUXmgP84fGs1asWkvxlcKA4iSaYBLuo8A--lNx1hDlGEvOqcfx5EbMs'
	
	tokenapp="cV5yiNqfQ5uggdLlfN9HNt:APA91bEndlNJJkRKiEH-ARcZE-BBnnK2RQF0WGQbBjFih6pmER5baDzTEt1NzqXraAXr3BEZukKGXbUdSRYuasyE4jGPjx83yl_Dve_w38yBTE07yWk7SehnKkPPNbuaRD7RTwRsWGV_"
	token_emu="dZMTCY5TQNCucoYJDEj183:APA91bGeVdEZ3MoBrG6TIsYePthD5fCaJAXr4CiTZQCXVQxQHWyq9zVjNuj2yV2JfiElsbHoyq6cVCGMiLakDEo8fq31tCdfpAQK4FrbKBeRdGMlKOenPp3o2MKCXZ8_a2c9KycHIKwZ"
	reg_id = "d-6ujEWLRX-O6bS3wmx6Im:APA91bGLiXqoQEVwSWq1fjh1yxZGpAam5b6Mm7T009CwF81Uq8IzSOb0ERLZtyJhLS2gzm2OL2Mm6aDJn_8BiVQxsuaSjMncpOIcQgP9luBSs9YkVz6XVErsj_USRu8qFvqJ5D6ohB3v"
	tokenoreo="ctqZRBo2S2-LLtgMhvmLJv:APA91bGkIqvmWS_8gdAuLysist_8n4XwlzSFLZ1x0gTogXWIiiRy946L6gnHFq_SmU8TbrFsvzCt-woHn3kVl1A5s_PdnIj3umhe9kwF7nm_YzO9k_ktdhaGzTrlmfjJqEIRDalKYXgg"
	token6tf="cSAuE8SWSqS7RTbyR4BTIY:APA91bH8RtNEQVfV0d9H55m_8VQVqydjwxRAkRHwIi5m0a9ed_-f7JR2wWunl7X-TIEV2hKS5a_HJniL6SgH9yot8xKmwXO-wXYogxlxIYkjWxNnACiOD0iFeKgDB7A7y4Abbo1qRMsw"
	tokenoreo2="dNToyE_-S1WbedBOw-pzAI:APA91bHsRM8CGX9hZ4M9L8isZ3y0S9EZGfB0EoHJCpX6xRbOb2zAfE43t8OOtJl7AP80T7fO96FyBSTBJ2zxhIY0mOsaLb8ZqcwCDsFwtxMzt5s2UeMsrICM_9Bun2J8UMv4aYEgkCpA"
	token2="dTOmJayjSnWEYruvSWOkcj:APA91bHz1vcqifaQezgHgcPMcClJ_OaIbwrOjWC_5TuPirOyxNTIMUP7bfrn8S1QXF5l5oWPtQ02q72lG7cN6UePdw8NoLzqXysEhCTyeI0JX7x2LXss3Pa3Pg52O-tz7TPwrW0YITjt"
	tokenfinal="f847aMr-R_mHoTw4HwAVcJ:APA91bHoYIbhrlo3TeQc2tMVqn8GY_gTxnrSvra5DW2fWsz46vSsJdn_zANygT_wT6566gFHoWn0VdIV5ZipUM8-387ZUyvex2W8JeyRJrko6CWECd1sAM0MrUf-x0iHw5pPhjFtVNEC"
	token1="dArapP2ZRcWyNyrdQQV6c7:APA91bHBsY5vf_uRCXVhDlU2YIo8JG16rrvKf9Z_5Rzv5JjlYMlU0Z_sMxk8RByacYBgtmr37ExaSvJCv8RdhEtau3tCDjsnvx49OOtITqCTfo3R0gpJ_KCu4DFOYhjsLPw_NeEg-lvR"
	if request.method=='POST':
		idalar=request.POST.get('serie')
		notu=request.POST.get('noty')
		if notu=='movimiento':
			movo=request.POST.get('gps')
			if movo is not None:
				indice = movo.find(',')
				latitud = movo[:indice]
				longitud = movo[indice +1:]
				datas={
					'serie':idalar,
					'tiponoti':notu, 
					'latitud':latitud, 
					'longitud':longitud}
				print("gps",latitud+" "+longitud)
		else:		
			datas={'tiponoti':notu}			
		if not firebase_admin._apps:
			cred = credentials.Certificate('static/carsafa-uni-firebase-adminsdk-ut950-f4f7d12592.json')
			firebase_admin.initialize_app(cred)
		
		message = messaging.Message(
		    data=datas,
		    token=tokenfinal,
		)
	response = messaging.send(message)
	print('Successfully sent message:', response)
	return HttpResponse('sappo')

# -----------------------fin para envio de notificacion----------------------------------

@csrf_exempt
def liberar_token(request):
	if request.method=='POST':
		to=request.POST.get('token')
		print("-----------gdfjfefff--f-ef----f-e-f--f", to)
		sd=Tokenfirebase.objects.filter(token=to)


		try:
			#Tokenfirebase.objects.filter(token=to).delete() #borra todo el registro
			Tokenfirebase.objects.filter(token=to).update(token="")
		except Exception as e:
			raise e

	return HttpResponse('ok')	


def vista_notificacion(request):
	return render(request, 'notificacion.html', locals())


