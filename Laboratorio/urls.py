from django.conf.urls import include, url
from django.contrib import admin
from . import  views

from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test, login_required
from django.conf.urls.static import static
from django.contrib.sessions.models import Session

Session.objects.all().delete()


app_name ='Laboratorio'

urlpatterns = [

#url(r'^subir_archivo/$', user_passes_test(views.primeroEnCola, login_url='/esperar/' )( views.Index ), name='Index'),
url(r'^index/$', user_passes_test(views.primeroEnCola, login_url='/esperar/' )( views.Index ), name='Index'),
url(r'^ingresar/$', login_required(views.Ingresar), name='Ingresar'),
#url(r'^laboratorio/$', user_passes_test(views.primeroEnCola, login_url='/esperar/')( views.Index ), name='Index'),
url(r'^laboratorio/$', login_required(views.Laboratorio, login_url='/esperar/'), name='Laboratorio'),


url(r'^subirArchivo/$', login_required(views.SubirArchivo, login_url='/esperar/'), name='Subir-Archivo'),
url(r'^compilar/$', login_required(views.Compilar) ,name='Compilar'),
url(r'^accionarBoton/$', views.AccionarBoton ,name='Accionar-Boton'),
url(r'^accionarAnalogo/$', views.AccionarAnalogo ,name='Accionar-Analogo'),

url(r'^esperar/$', login_required(views.Esperar), name='Esperar'),
url(r'^login/$', views.Login, name='Login'),

#url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='Login'),
url(r'^logout/$', auth_views.logout, {'next_page': 'Laboratorio:Login'}, name='Logout'),

url(r'^actualizarTiempos/$', views.ActualizarTiempos ,name='Actualizar-Tiempos'),
url(r'^actualizarUsuario/$', views.ActualizarUsuario ,name='Actualizar-Usuario'),


]

