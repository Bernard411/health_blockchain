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
from django.shortcuts import render, redirect
from .models import MedicalRecord, Patient
from django.contrib.auth.decorators import login_required
from web3 import Web3
from django.conf import settings
from web3 import Account



def login_view(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('headoffice')
            elif user.groups.filter(name='patients').exists():
                return redirect('manage_health_records_x')
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


@login_required
def home(request):
    return render(request, 'doctors/home_content.html')


@login_required
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
import uuid  # Import uuid for generating a unique blockchain ID

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
            insurance_number=insurance_number,
            blockchain_id=str(uuid.uuid4())  # Generate a unique blockchain ID
        )
        patient.save()
        
        # Redirect to the patient list after adding
        return redirect('login')

    return render(request, 'registration.html')



from django.shortcuts import render
from .models import Patient, LabTest, MedicalRecord
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Import Paginator

@login_required
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

@login_required
def manage_health_records(request):
    medical_records = MedicalRecord.objects.all()
    paginator = Paginator(medical_records, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        
        'patients': patients,
    }
   
    return render(request, 'doctors/manage_health_records.html', context)


from django.shortcuts import render
from .models import MedicalRecord, Patient
@login_required
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
    paginator = Paginator(medical_records, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        
        'patients': patients,
    }
 

    # Render the template with the medical records
    return render(request, 'patient/manage_health_records.html', context)


@login_required
def manage_preceptions(request):
    preceptions = Prescription.objects.all()
    paginator = Paginator(preceptions, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        
        'patients': patients,
    }
    
    return render(request, 'doctors/prescription.html', context)


def patients(request):
    return render(request, 'patient/home_content.html')







# Connect to the blockchain (assuming you have configured INFURA/other provider in your settings)
web3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_PROVIDER_URL))

# Load your contract ABI and address (these should be stored in settings or another secure location)
CONTRACT_ABI = settings.CONTRACT_ABI
CONTRACT_ADDRESS = settings.CONTRACT_ADDRESS

@login_required
def add_medical_record(request):
    if request.method == "POST":
        # Gather data from the form
        patient_id = request.POST.get("patient")
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")
        
        patient = Patient.objects.get(id=patient_id)
        doctor = request.user  # Assuming the authenticated user is the doctor
        
        # Ensure the patient has a blockchain ID
        if not patient.blockchain_id:
            print(f"Error: Patient {patient_id} has no blockchain ID.")
            return render(request, 'doctors/add_medical_record.html', {
                'patients': Patient.objects.all(),
                "error": "Patient does not have a blockchain ID."
            })
        
        # Create the medical record in Django (Database)
        medical_record = MedicalRecord.objects.create(
            patient=patient,
            doctor=doctor,
            diagnosis=diagnosis,
            treatment=treatment
        )
        
        # Convert UUID to a uint256 (integer) to pass to the smart contract
        blockchain_id_int = int(patient.blockchain_id.replace('-', ''), 16)  # Convert UUID to integer

        # Add the record to the blockchain
        try:
            contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
            account = Account.from_key(settings.DOCTOR_PRIVATE_KEY)  # Correct method for creating account
            nonce = web3.eth.get_transaction_count(account.address)

            # Build the transaction manually
            txn = {
                'chainId': 11155111,  # Sepolia testnet ID
                'gas': 2000000,
                'gasPrice': web3.to_wei(20, 'gwei'),  # Use to_wei for converting Gwei to Wei
                'nonce': nonce,
            }

            # Call the contract function with arguments and build the transaction
            txn_data = contract.functions.addRecord(
                blockchain_id_int,  # Converted to uint256
                diagnosis,
                treatment
            ).build_transaction(txn)  # Use build_transaction with an underscore

            # Sign the transaction
            signed_txn = web3.eth.account.sign_transaction(txn_data, private_key=settings.DOCTOR_PRIVATE_KEY)
            
            # Send the transaction to the blockchain
            txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)  # Use raw_transaction with an underscore
            
            # Wait for transaction receipt
            txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

            # If successful, save blockchain reference (transaction hash) to the medical record
            medical_record.blockchain_reference = txn_hash.hex()
            medical_record.save()

            # Redirect after successfully adding the record
            return redirect('manage_health_records')
        
        except Exception as e:
            # Handle errors (log or display to the user)
            print(f"An error occurred while adding the record to the blockchain: {e}")
            return render(request, 'doctors/add_medical_record.html', {
                'patients': Patient.objects.all(),
                "error": "Failed to add medical record to the blockchain."
            })

    # Load data for form display
    medical_records = MedicalRecord.objects.all()
    patients = Patient.objects.all()
    paginator = Paginator(medical_records, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    patient = Patient.objects.all()
    context = {
        'page_obj': page_obj,
        
        'patients': patients,
    }
    return render(request, 'doctors/add_medical_record.html', context)



from django.shortcuts import render, redirect
from .models import Prescription, MedicalRecord
@login_required
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
    medical_records = MedicalRecord.objects.all()
    paginator = Paginator(medical_records, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        "medical_records" : medical_records,
        
        'patients': patients,
    }
    return render(request, 'doctors/add_prescription.html', context)

from django.shortcuts import render, redirect
from .models import Appointment, Patient
@login_required
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

@login_required

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
    medical_records = MedicalRecord.objects.all()
    billing= Billing.objects.all()
    paginator = Paginator(billing, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    patients = Patient.objects.all()
   
    context = {
        'page_obj': page_obj,
        "medical_records" : medical_records,
        'patients': patients,
    }
    
    return render(request, 'doctors/add_billing.html', context)


from django.shortcuts import render, redirect
from .models import LabTest, MedicalRecord
@login_required
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
    medical_records = MedicalRecord.objects.all()
    test = LabTest.objects.all()
    paginator = Paginator(test, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        "medical_records" : medical_records
    }
    return render(request, 'doctors/add_lab_test.html', context)



from django.shortcuts import render, get_object_or_404
from .models import MedicalRecord, Prescription, Appointment, Billing, LabTest

def view_medical_record(request, record_id):
    # Retrieve the medical record
    medical_record = get_object_or_404(MedicalRecord, id=record_id)
    
    # Retrieve associated data
    prescriptions = Prescription.objects.filter(medical_record=medical_record)
    appointments = Appointment.objects.filter(patient=medical_record.patient)
    billing_info = Billing.objects.filter(medical_record=medical_record).first()  # Assuming one billing record per medical record
    lab_tests = LabTest.objects.filter(medical_record=medical_record)

    context = {
        'medical_record': medical_record,
        'prescriptions': prescriptions,
        'appointments': appointments,
        'billing_info': billing_info,
        'lab_tests': lab_tests,
    }

    return render(request, 'doctors/view_medical_record.html', context)


from django.shortcuts import render
from .models import MedicalRecord  # Assuming you're searching in MedicalRecord

def search_records(request):
    query = request.GET.get('table_search', '')
    results = MedicalRecord.objects.filter(patient__name__icontains=query)  # Adjust this based on your search criteria
    return render(request, 'doctors/x.html', {'results': results, 'query': query})


def view_medical_record_x(request, record_id):
    # Retrieve the medical record
    medical_record = get_object_or_404(MedicalRecord, id=record_id)
    
    # Retrieve associated data
    prescriptions = Prescription.objects.filter(medical_record=medical_record)
    appointments = Appointment.objects.filter(patient=medical_record.patient)
    billing_info = Billing.objects.filter(medical_record=medical_record).first()  # Assuming one billing record per medical record
    lab_tests = LabTest.objects.filter(medical_record=medical_record)

    context = {
        'medical_record': medical_record,
        'prescriptions': prescriptions,
        'appointments': appointments,
        'billing_info': billing_info,
        'lab_tests': lab_tests,
    }

    return render(request, 'patient/view_medical_record.html', context)


from django.shortcuts import render
from .models import MedicalRecord  # Assuming you're searching in MedicalRecord

def search_records_x(request):
    query = request.GET.get('table_search', '')
    results = MedicalRecord.objects.filter(patient__name__icontains=query)  # Adjust this based on your search criteria
    return render(request, 'patient/x.html', {'results': results, 'query': query})


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from .forms import UserRegistrationForm, PatientRegistrationForm
from .models import Patient

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        patient_form = PatientRegistrationForm(request.POST)
        
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  # Hash the password
            user.save()

            # Create a Patient instance
            patient = patient_form.save(commit=False)
            patient.user = user  # Associate the patient with the user
            patient.save()

            # Generate blockchain ID
            patient.blockchain_id = str(uuid.uuid4())
            patient.save()

            # Add user to the Patient group
            patient_group = Group.objects.get(name='patients')
            patient_group.user_set.add(user)

            # Log the user in
            login(request, user)
            return redirect('login')  # Change to your desired redirect

    else:
        user_form = UserRegistrationForm()
        patient_form = PatientRegistrationForm()
    
    return render(request, 'register.html', {'user_form': user_form, 'patient_form': patient_form})



# views.py
import qrcode
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO

def generate_qr_code(request, record_id):
    url = request.build_absolute_uri(f"/view_medical_record/{record_id}")
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")
