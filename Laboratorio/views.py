from django.shortcuts import render
from django.http import HttpResponse
from gpiozero import LED
from django.core.files.storage import FileSystemStorage
import os
import json
from django.conf import settings

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


def Index(request):
	#if request.GET["pin04"]:

	return render(request, 'Laboratorio/subir_archivo.html')


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
                'uploaded_file_url': uploaded_file_url, 'exito': True,
            })
        return render(request, 'Laboratorio/subir_archivo.html', {
                'uploaded_file_url': "El archivo debe tener extensión .ino", 'exito': False,
            })

    return render(request,  'Laboratorio/subir_archivo.html')

import time
def Compilar(request):
    print('compilar req')
    if request.is_ajax():
        print('is ajax')
        currentdir =os.path.dirname(os.path.abspath(__file__))
        print ('base'+ str(currentdir))
        os.chdir(settings.MEDIA_ROOT)
        
        time.sleep(60)
        #salida= os.popen('bash make.sh').read()
        os.chdir(currentdir)
        #print (salida)
        results='true'
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)