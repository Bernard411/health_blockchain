from django.shortcuts import render
from .models import *
# Create your views here.
from django.core.paginator import Paginator

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from .models import *



def login_view(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('headoffice')
            elif user.groups.filter(name='patients').exists():
                return redirect('officers')
            elif user.groups.filter(name='doctors').exists():
                return redirect('patients_database')
            else:
                messages.error(request, "Invalid Login!")
                return render(request, 'login.html')
        else:
            messages.error(request, "Invalid Login Credentials!")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    



def logoutuser(request):
    logout(request)
    return redirect('login')



def home(request):
    return render(request, 'home_content.html')



def patients_database(request):
    patients = Patient.objects.all() 
    paginator = Paginator(patients, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        
        'patients': patients,
    }
 
    return render(request, 'patients_database.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Patient
import random
from faker import Faker

def add_patients(request):
    if request.method == 'POST':
        # Create user
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        user = User.objects.create_user(username=username, password=password, email=email)
        
        # Patient details
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        emergency_contact = request.POST.get('emergency_contact')
        insurance_provider = request.POST.get('insurance_provider')
        insurance_number = request.POST.get('insurance_number')

        # Create Patient instance
        patient = Patient(
            user=user,
            name=name,
            dob=dob,
            gender=gender,
            address=address,
            phone=phone,
            emergency_contact=emergency_contact,
            insurance_provider=insurance_provider,
            insurance_number=insurance_number
        )
        patient.save()
        
        # Redirect to the patient list after adding
        return redirect('patient_list')

    return render(request, 'registration.html')


def manage_patients(request):
    # Logic to retrieve and manage patient records
    return render(request, 'manage_patients.html', context={})

def add_health_records(request):
    if request.method == 'POST':
        # Logic to add health records
        pass
    return render(request, 'add_health_records.html', context={})

def manage_health_records(request):
    # Logic to retrieve and manage health records
    return render(request, 'manage_health_records.html', context={})
