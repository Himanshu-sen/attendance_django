from django.contrib import admin
from django.urls import path
from home import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.index,name='home'),
    path('upload', views.upload,name='upload'),
    path('submit', views.submit,name='submit'),
    path('logoutuser', views.logoutuser,name='logoutuser'),    
    path('contact', views.contact,name='contact'),
    path('take_attendance/', views.take_attendance,name='take_attendance'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico'))),
    path('loginuser', views.loginuser,name='loginuser'),


]