from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dob = models.DateField()  # Date of birth
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.TextField()
    phone = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    insurance_provider = models.CharField(max_length=100, null=True, blank=True)
    insurance_number = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.name




class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    date_of_visit = models.DateTimeField(auto_now_add=True)
    blockchain_reference = models.CharField(max_length=255, null=True, blank=True)  # To store blockchain transaction or hash
    
    def __str__(self):
        return f"Record for {self.patient.name}"


class Prescription(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    drug_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    additional_instructions = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.drug_name} for {self.medical_record.patient.name}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])

    def __str__(self):
        return f"Appointment for {self.patient.name} with {self.doctor.name} on {self.appointment_date}"

class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')])
    payment_date = models.DateTimeField(null=True, blank=True)
    transaction_reference = models.CharField(max_length=100, null=True, blank=True)  # Store blockchain or payment gateway transaction reference

    def __str__(self):
        return f"Billing for {self.patient.name} - Status: {self.payment_status}"

class HealthcareProvider(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    license_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class LabTest(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    result = models.TextField(null=True, blank=True)
    date_conducted = models.DateTimeField(auto_now_add=True)
    conducted_by = models.CharField(max_length=100)

    def __str__(self):
        return f"Lab Test: {self.test_name} for {self.medical_record.patient.name}"


class BlockchainTransaction(models.Model):
    transaction_hash = models.CharField(max_length=255)
    related_record = models.CharField(max_length=100)  # Could reference MedicalRecord, Prescription, etc.
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction: {self.transaction_hash} at {self.timestamp}"
