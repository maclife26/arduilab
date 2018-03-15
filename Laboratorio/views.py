
from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse

from gpiozero import LED
import RPi.GPIO as GPIO

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import os
import time
import json
from django.conf import settings



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18, GPIO.OUT)
verde = GPIO.PWM(18, 100)




btn2 = LED(17)

'''btn1 = LED(4)

btn3 = LED(6)
btn4 = LED(12)
btn5 = LED(13)
'''
#btn6 = LED(17)
#btn7 = LED(18)
#btn8 = LED(22)
# Create your views here.




def superuser(user):
    return user.is_superuser

def superuser_or_profesor(user):
    return user.is_superuser or user.groups.filter(name='Profesor').exists()


def Index(request):
	#if request.GET["pin04"]:

	return render(request, 'Laboratorio/laboratorio.html')


def Pin02(request):
	if 'on1' in request.POST:
		btn2.on()
	elif 'off1' in request.POST:
		btn2.off()
	return render(request, 'Laboratorio/principal.html')

class MyFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if os.path.exists(self.path(name)):
            os.remove(self.path(name))
        return name

#Envío de archivo .ino al servidor
def SubirArchivo(request):       
    if request.method == 'POST' and request.FILES.get('exampleInputFile'):
        myfile = request.FILES['exampleInputFile']
        if str(myfile.name).endswith(".ino"):

            fs = MyFileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print(filename)
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)
            return render(request, 'Laboratorio/subir_archivo.html', {
                'uploaded_file_url': "Archivo subido satisfactoriamente", 'exito': True,
            })
        return render(request, 'Laboratorio/subir_archivo.html', {
                'uploaded_file_url': "El archivo debe tener extensión .ino", 'exito': False,
            })

    return render(request,  'Laboratorio/subir_archivo.html')

import subprocess

def Compilar(request):
    print('compilar req')
    if request.is_ajax():
        currentdir =os.path.dirname(os.path.abspath(__file__))
        print ('base'+ str(currentdir))
        os.chdir(settings.MEDIA_ROOT)
        
        #time.sleep(20)
        salidaCompilacion= subprocess.call('bash make2.sh', shell=True, cwd='/home/pi/projects/arduilab/media/sketchbook/')
        #salida= subprocess.Popen('bash monitor.sh', shell=True, cwd='/home/pi/projects/arduilab/media/sketchbook/').read()
        #time.sleep(15)
        #print (salida)
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

        verde.start(0)

        if "ana1" in saludo:       
            results = (int(results)*1.00)
            verde.ChangeDutyCycle(results)
            
        elif "ana2" in saludo:        
            results = (int(results)*1.00)
            verde.ChangeDutyCycle(results)
               
    return HttpResponse(status=200)