from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home_content.html')



def patients_database(request):
    # Logic to retrieve patients from the database
    return render(request, 'patients_database.html', context={})

def add_patients(request):
    if request.method == 'POST':
        # Logic to add a new patient
        pass
    return render(request, 'add_patients.html', context={})

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
