from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView



from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', views.home, name="home")
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


