from django.conf.urls import include, url
from django.contrib import admin
from . import  views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test


app_name ='Laboratorio'

urlpatterns = [
#url(r'^$', views.Index ,name='Index'),
url(r'^sketch/$', views.Sketch ,name='Sketch'),
url(r'^$', views.Pin02 ,name='Pin02'),


url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='Login'),
url(r'^logout/$', auth_views.logout, {'next_page': 'Laboratorio:Inicio'}, name='Logout'),


]