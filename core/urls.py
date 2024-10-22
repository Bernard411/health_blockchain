from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView



from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', views.login_view, name='login'),
  path('logout/', views.logoutuser, name='logout'),

  path('patients-database/', views.patients_database, name='patients_database'),
  path('add-patients/', views.add_patients, name='add_patients'),
  path('manage-patients/', views.manage_patients, name='manage_patients'),
  path('add-health-records/', views.add_health_records, name='add_health_records'),
  path('manage-health-records/', views.manage_health_records, name='manage_health_records'),


  path('home/patients/', views.patients, name='patients'),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


