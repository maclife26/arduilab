from django.conf.urls import include, url
from django.contrib import admin
from . import  views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test
from django.conf.urls.static import static


app_name ='Laboratorio'

urlpatterns = [
url(r'^subir_archivo/$', views.SubirArchivo ,name='Subir-Archivo'),
url(r'^$', views.Pin02 ,name='Pin02'),
url(r'^laboratorio/$', views.Index ,name='Index'),

url(r'^compilar/$', views.Compilar ,name='Compilar'),
url(r'^accionarBoton/$', views.AccionarBoton ,name='Accionar-Boton'),
url(r'^accionarAnalogo/$', views.AccionarAnalogo ,name='Accionar-Analogo'),


url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='Login'),
url(r'^logout/$', auth_views.logout, {'next_page': 'registration/logout.html'}, name='Logout'),


]