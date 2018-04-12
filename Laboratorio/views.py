
from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm

from gpiozero import LED
import RPi.GPIO as GPIO

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import scheduler
import os
import time
import json
import datetime
import shutil
import subprocess






GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18, GPIO.OUT)
#COLOCAR EL OTRO ANALÓGICO
firts = GPIO.PWM(18, 100) #23
#second = GPIO.PWM(24, 100)


btn2 = LED(17)
'''
btn1 = LED(4)

btn3 = LED(6)
btn4 = LED(12)
btn5 = LED(13)

#btn6 = LED(17)
#btn7 = LED(18)
#btn8 = LED(22)
# Create your views here.
'''



TiempoRestante=settings.TIEMPO_DE_SERVICIO
Cola=[]

##queryset de usuarios 
def obtener_usuarios_qs():
    sesiones_actuales = Session.objects.filter(expire_date__gte=timezone.now())
    lista_usuarios = []
    for session in sesiones_actuales:
        sesion = session.get_decoded()
        lista_usuarios.append(sesion.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return User.objects.filter(id__in=lista_usuarios)

def obtener_lista_usuarios():
    usuarios_qs=obtener_usuarios_qs()
    lista = list(usuarios_qs.values_list('username', flat=True))
    return lista

def rotar(l, n):
    return l[n:] + l[:n]


def actualizarCola(superuser=False, staff=False):
    global Cola
    global TiempoRestante
    lista=obtener_lista_usuarios()
    desconectados= [x for x in Cola if x not in lista]
    nuevos= [x for x in lista if x not in Cola]

    if desconectados and not superuser:
        if Cola[0] in desconectados:
            TiempoRestante=settings.TIEMPO_DE_SERVICIO
        print('desconectados')
        Cola=[item for item in Cola if item not in desconectados]
    if nuevos:
        Cola=Cola+nuevos
        print('nuevos')


def caminarCola():
    global Cola
    Cola=rotar(Cola,1)
    
def tiempoUsuario(user):
    actualizarCola()
    global Cola
    posicion=Cola.index(user) + 1
    if (posicion==1 or posicion==2 ):
        return (TiempoRestante)
    elif(posicion>2):
        return (TiempoRestante + ((posicion-2) * settings.TIEMPO_DE_SERVICIO))
    
def Esperar(request):
    context={'tiempo':tiempoUsuario(request.user.username), 'colaUsuario':Cola}
    return render(request, 'Laboratorio/cola.html',context)

def Login(request):
    global Cola
    global TiempoRestante
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not Cola:
                TiempoRestante=settings.TIEMPO_DE_SERVICIO
                actualizarCola()
                return redirect (reverse_lazy("Laboratorio:Index"))
            else:
                if user.is_superuser or user.is_staff:
                    TiempoRestante=settings.TIEMPO_DE_SERVICIO
                    Cola.insert(0,str(user))       
                    actualizarCola(True)
                return redirect (reverse_lazy("Laboratorio:Esperar"))
        else:
            return render(request, "registration/login.html", {'error': "Usuario o contraseña incorrecto"})
    return render(request, "registration/login.html", )    

def superuser(user):
    return user.is_superuser

def staff(user):
    return user.is_staff

def superuser_or_profesor(user):
    return user.is_superuser or user.groups.filter(name='Profesor').exists()

def primeroEnCola(user):
    actualizarCola()
    encola=""
    try:
        encola=str(Cola[0])
    except IndexError as e:
        encola=""
        return False
    if encola==str(user):
        return True
    return False


def relojServicio():
    global TiempoRestante
    if(TiempoRestante>1):
        TiempoRestante=TiempoRestante-1
    elif(Cola):
        caminarCola()
        TiempoRestante=settings.TIEMPO_DE_SERVICIO
    else:
        pass
        #job_relojServicio.pause()

job_relojServicio=scheduler.add_job(relojServicio, 'interval', seconds=1, id='job_relojServicio')


def ActualizarTiempos(request):
    if request.is_ajax():
        print('usuario:'+str(request.user))
        res=[tiempoUsuario(request.user.username), len(Cola)-1]
        data = json.dumps(res)
    else:
        data = 'fail'
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)


def ActualizarUsuario(request):
    if request.is_ajax():
        user=request.user
        if primeroEnCola(user):
            res=True
        else:
            res=False
        data = json.dumps(res)
    else:
        data = 'fail'
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)


def Index(request):
	context={'tiempo':tiempoUsuario(request.user.username), 'cola': len(Cola)-1 }
	return render(request, 'Laboratorio/index.html',context )

def Laboratorio(request):
    context={'tiempo':tiempoUsuario(request.user.username), 'cola': len(Cola)-1 }
    return render(request, 'Laboratorio/laboratorio.html', context)

def Ingresar(request):
    if request.method == 'POST':
        return redirect(reverse_lazy("Laboratorio:Subir-Archivo"))


class MyFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if os.path.exists(self.path(name)):
            os.remove(self.path(name))
        return name


#Envío de archivo .ino al servidor y respaldos
def SubirArchivo(request):  
    if request.method == 'POST' and request.FILES.get('exampleInputFile'):
        myfile = request.FILES['exampleInputFile']
        if str(myfile.name).endswith(".ino"):

            fs = MyFileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            respaldosDir = 'Respaldos'
            fecha= datetime.datetime.now().strftime("%d_%m_%y %H %M")
            src_dir=fs.path(myfile.name)
            nombre_archivo='/{0}_{1}_{2}'.format(fecha, request.user, myfile.name)
            des_dir = os.path.join(settings.MEDIA_ROOT, respaldosDir+nombre_archivo)
            shutil.copy2(src_dir,des_dir)
            
            return render(request, 'Laboratorio/subir_archivo.html', {
                'uploaded_file_url': "Archivo subido satisfactoriamente", 'exito': True,
            })
        return render(request, 'Laboratorio/subir_archivo.html', {
                'uploaded_file_url': "El archivo debe tener extensión .ino", 'exito': False,
            })

    return render(request,  'Laboratorio/subir_archivo.html')


def Compilar(request):
    if request.is_ajax():
        currentdir = os.path.dirname(os.path.abspath(__file__))
        print ('base'+ str(currentdir))
        os.chdir(settings.MEDIA_ROOT)      
        salidaCompilacion= subprocess.call('bash make.sh', shell=True, cwd='/home/pi/projects/arduilab/media/sketchbook/')
        results='true'
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)



def AccionarBoton(request):
    if request.is_ajax():
        results=request.GET.get('peticion')
        
        data = json.dumps(results)
        print (data)
        
        if "on1" in data:
            btn1.on()
        elif "off1" in data:
            btn1.off()
        elif "on2" in data:
            btn2.on()
        elif "off2" in data:
            btn2.off()
        elif "on3" in data:
            btn3.on()
        elif "off3" in data:
            btn3.off()
        elif "on4" in data:
            btn4.on()
        elif "off4" in data:
            btn4.off()
        elif "on5" in data:
            btn5.on()
        elif "off5" in data:
            btn5.off()
        elif "on6" in data:
            btn7.on()
        elif "off6" in data:
            btn6.off()
        elif "on7" in data:
            btn7.on()
        elif "off7" in data:
            btn7.off()
        elif "on8" in data:
            btn8.on()
        elif "off8" in data:
            btn8.off()        
    else:
        data = 'fail'
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)


def AccionarAnalogo(request):
    if request.is_ajax():     
        results=request.GET.get('peticionA')
        saludo=request.GET.get('saludo')

        firts.start(0)

        if "ana1" in saludo:       
            results = (int(results)*1.00)
            firts.ChangeDutyCycle(results)
            
        elif "ana2" in saludo:        
            results = (int(results)*1.00)
            firts.ChangeDutyCycle(results)
               
    return HttpResponse(status=200)