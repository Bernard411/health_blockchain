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

  path('manage-health-records/', views.manage_health_records, name='manage_health_records'),
  path('manage-health-records/patient/', views.manage_health_records_patient, name='manage_health_records_x'),
  path('home/patients/', views.patients, name='patients'),

    path('add-medical-record/', views.add_medical_record, name='add_medical_record'),
    path('add-prescription/', views.add_prescription, name='add_prescription'),
    path('add-appointment/', views.add_appointment, name='add_appointment'),
    path('add-billing/', views.add_billing, name='add_billing'),
    # path('add-healthcare-provider/', views.add_healthcare_provider, name='add_healthcare_provider'),
    path('add-lab-test/', views.add_lab_test, name='add_lab_test'),
    path('preceptions/', views.manage_preceptions, name='preceptions'),

 path('medical-record/<int:record_id>/', views.view_medical_record, name='view_medical_record'),
 path('search/', views.search_records, name='search_records'),
 path('medical-record/patient/<int:record_id>/', views.view_medical_record_x, name='view_medical_record_x'),
 path('search/patient', views.search_records_x, name='search_records_x'),
 path('register/', views.register, name='register'),

 path('generate_qr_code/<int:record_id>/', views.generate_qr_code, name='generate_qr_code'),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


