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
                return redirect('patients')
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
    return render(request, 'doctors/home_content.html')



def patients_database(request):
    patients = Patient.objects.all() 
    paginator = Paginator(patients, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        
        'patients': patients,
    }
 
    return render(request, 'doctors/patients_database.html', context)


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



from django.shortcuts import render
from .models import Patient, LabTest, MedicalRecord
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Import Paginator

def manage_patients(request):
    patients = Patient.objects.all()  # Fetch all patients
    patient_data = []

    for patient in patients:
        # Count the number of lab tests associated with each patient
        num_tests = LabTest.objects.filter(medical_record__patient=patient).count()
        
        patient_data.append({
            'patient': patient,
            'num_tests': num_tests,
        })

    # Set up pagination
    paginator = Paginator(patient_data, 8)  # Show 8 patients per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range (e.g. 999), deliver last page of results
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'doctors/manage_patients.html', {'page_obj': page_obj})


def manage_health_records(request):
    medical_records = MedicalRecord.objects.all()
    context = {
        "medical_records" : medical_records
    }
    return render(request, 'doctors/manage_health_records.html', context)


from django.shortcuts import render
from .models import MedicalRecord, Patient

def manage_health_records_patient(request):
    # Get the authenticated user
    user = request.user
    
    # Try to get the associated Patient instance
    try:
        patient = user.patient  # Assuming the User has a OneToOne relationship with Patient
    except Patient.DoesNotExist:
        # If the patient does not exist, you can handle it here (e.g., redirect or show a message)
        return render(request, 'patient/manage_health_records.html', {
            'medical_records': [],
            'message': 'No patient record found for your account.'
        })

    # Get medical records associated with the patient
    medical_records = MedicalRecord.objects.filter(patient=patient)

    # Render the template with the medical records
    return render(request, 'patient/manage_health_records.html', {
        'medical_records': medical_records
    })




def manage_preceptions(request):
    preceptions = Prescription.objects.all()
    context = {
        "preceptions" : preceptions
    }
    return render(request, 'doctors/prescription.html', context)


def patients(request):
    return render(request, 'patient/home_content.html')



from django.shortcuts import render, redirect
from .models import MedicalRecord, Patient
from django.contrib.auth.decorators import login_required

@login_required
def add_medical_record(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient")
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")
        blockchain_reference = request.POST.get("blockchain_reference")
        
        patient = Patient.objects.get(id=patient_id)
        doctor = request.user  # Assuming the authenticated user is the doctor

        MedicalRecord.objects.create(
            patient=patient,
            doctor=doctor,  # Assuming doctor is a foreign key to the user
            diagnosis=diagnosis,
            treatment=treatment,
            blockchain_reference=blockchain_reference
        )
        return redirect('manage_health_records')
    
    medical_records = MedicalRecord.objects.all()
    
    
    return render(request, 'doctors/add_medical_record.html', {'patients': Patient.objects.all(), "medical_records": medical_records} )


from django.shortcuts import render, redirect
from .models import Prescription, MedicalRecord

def add_prescription(request):
    if request.method == "POST":
        medical_record_id = request.POST.get("medical_record")
        drug_name = request.POST.get("drug_name")
        dosage = request.POST.get("dosage")
        frequency = request.POST.get("frequency")
        duration = request.POST.get("duration")
        additional_instructions = request.POST.get("additional_instructions")
        
        medical_record = MedicalRecord.objects.get(id=medical_record_id)

        Prescription.objects.create(
            medical_record=medical_record,
            drug_name=drug_name,
            dosage=dosage,
            frequency=frequency,
            duration=duration,
            additional_instructions=additional_instructions
        )
        return redirect('preceptions')
    return render(request, 'doctors/add_prescription.html', {'medical_records': MedicalRecord.objects.all()})

from django.shortcuts import render, redirect
from .models import Appointment, Patient

def add_appointment(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient")
        # doctor_id = request.POST.get("doctor")
        appointment_date = request.POST.get("appointment_date")
        reason = request.POST.get("reason")
        status = request.POST.get("status")

        patient = Patient.objects.get(id=patient_id)
        # doctor = Doctor.objects.get(id=doctor_id)

        Appointment.objects.create(
            patient=patient,
            # doctor=doctor,
            appointment_date=appointment_date,
            reason=reason,
            status=status
        )
        return redirect('success_page')
    return render(request, 'doctors/add_appointment.html', {'patients': Patient.objects.all()})


from django.shortcuts import render, redirect
from .models import Billing, Patient, MedicalRecord

def add_billing(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient")
        medical_record_id = request.POST.get("medical_record")
        total_amount = request.POST.get("total_amount")
        paid_amount = request.POST.get("paid_amount")
        payment_status = request.POST.get("payment_status")
        payment_date = request.POST.get("payment_date")
        transaction_reference = request.POST.get("transaction_reference")

        patient = Patient.objects.get(id=patient_id)
        medical_record = MedicalRecord.objects.get(id=medical_record_id)

        Billing.objects.create(
            patient=patient,
            medical_record=medical_record,
            total_amount=total_amount,
            paid_amount=paid_amount,
            payment_status=payment_status,
            payment_date=payment_date,
            transaction_reference=transaction_reference
        )
        return redirect('add_billing')
    
    return render(request, 'doctors/add_billing.html', {'patients': Patient.objects.all(), 'medical_records': MedicalRecord.objects.all(), 'billing': Billing.objects.all()})


from django.shortcuts import render, redirect
from .models import LabTest, MedicalRecord

def add_lab_test(request):
    if request.method == "POST":
        medical_record_id = request.POST.get("medical_record")
        test_name = request.POST.get("test_name")
        result = request.POST.get("result")
        conducted_by = request.POST.get("conducted_by")
        
        medical_record = MedicalRecord.objects.get(id=medical_record_id)

        LabTest.objects.create(
            medical_record=medical_record,
            test_name=test_name,
            result=result,
            conducted_by=conducted_by
        )
        return redirect('add_lab_test')
    return render(request, 'doctors/add_lab_test.html', {'medical_records': MedicalRecord.objects.all(), 'test': LabTest.objects.all()})
