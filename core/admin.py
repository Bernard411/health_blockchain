from django.contrib import admin
from .models import Patient, Doctor, MedicalRecord, Prescription, Appointment, Billing, HealthcareProvider, LabTest, BlockchainTransaction

# Customizing the admin interface for each model

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'dob', 'gender', 'phone', 'insurance_provider')  # Display key fields in the list view
    search_fields = ('name', 'phone')  # Enable search functionality for patient name and phone
    list_filter = ('gender', 'insurance_provider')  # Add filters for gender and insurance provider
    ordering = ('name',)  # Default ordering by name

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'phone', 'license_number')  # Display key fields in the list view
    search_fields = ('name', 'specialization', 'license_number')  # Enable search functionality for name and license number
    ordering = ('name',)  # Default ordering by name

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'diagnosis', 'date_of_visit')  # Show these fields in the list view
    search_fields = ('patient__name', 'doctor__name', 'diagnosis')  # Enable search for patient, doctor, and diagnosis
    list_filter = ('date_of_visit',)  # Add filter for visit date
    ordering = ('-date_of_visit',)  # Order by visit date descending
    readonly_fields = ('blockchain_reference',)  # Prevent editing of blockchain reference

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'drug_name', 'dosage', 'duration')  # Display prescription info
    search_fields = ('medical_record__patient__name', 'drug_name')  # Enable search for patient and drug name
    list_filter = ('medical_record__patient', 'medical_record__doctor')  # Filter by patient and doctor
    ordering = ('medical_record__patient',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'status')  # Display key fields in the list view
    search_fields = ('patient__name', 'doctor__name', 'reason')  # Enable search functionality
    list_filter = ('status', 'appointment_date')  # Add filters for status and appointment date
    ordering = ('-appointment_date',)  # Order by appointment date descending

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medical_record', 'total_amount', 'paid_amount', 'payment_status', 'payment_date')  # Billing info
    search_fields = ('patient__name', 'medical_record__doctor__name')  # Search by patient or doctor name
    list_filter = ('payment_status', 'payment_date')  # Filter by payment status and date
    ordering = ('-payment_date',)  # Order by payment date descending
    readonly_fields = ('transaction_reference',)  # Prevent editing of transaction reference

@admin.register(HealthcareProvider)
class HealthcareProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'license_number')  # Display healthcare provider details
    search_fields = ('name', 'license_number')  # Enable search for name and license number
    ordering = ('name',)

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'test_name', 'result', 'date_conducted')  # Display lab test details
    search_fields = ('medical_record__patient__name', 'test_name')  # Enable search for patient and test name
    list_filter = ('date_conducted',)  # Filter by test date
    ordering = ('-date_conducted',)  # Order by test date descending

@admin.register(BlockchainTransaction)
class BlockchainTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_hash', 'related_record', 'timestamp')  # Display blockchain transaction details
    search_fields = ('transaction_hash', 'related_record')  # Enable search for transaction hash or related record
    list_filter = ('timestamp',)  # Filter by timestamp
    ordering = ('-timestamp',)  # Order by timestamp descending
