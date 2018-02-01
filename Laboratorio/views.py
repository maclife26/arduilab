from django.shortcuts import render
from django.http import HttpResponse
from gpiozero import LED


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

	return render(request, 'Laboratorio/base.html')

#Seguir desarrollando este método para poder enviar el Sketch hasta la Placa Arduino
def Sketch(request):
	if 'sketch' in request.POST:
		println('enviado')
	else:
		println('no se ha podido enviar')
	return render(request, 'Laboratorio/base.html')

def Pin02(request):
	if 'on1' in request.POST:
		btn2.on()
	elif 'off1' in request.POST:
		btn2.off()
	return render(request, 'Laboratorio/base.html')


