from django.contrib import admin
from .models import Patient,  MedicalRecord, Prescription, Appointment, Billing, HealthcareProvider, LabTest, BlockchainTransaction

# Customizing the admin interface for each model
from django.contrib import admin
from .models import Patient, MedicalRecord, Prescription, Appointment, Billing, HealthcareProvider, LabTest, BlockchainTransaction

# Registering the Patient model
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'dob', 'gender', 'phone', 'emergency_contact', 'insurance_provider')
    search_fields = ('name', 'phone', 'insurance_provider')
    list_filter = ('gender', 'dob')

# Registering the MedicalRecord model
@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'diagnosis', 'date_of_visit', 'blockchain_reference')
    search_fields = ('patient__name', 'doctor__username', 'diagnosis')
    list_filter = ('date_of_visit',)

# Registering the Prescription model
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'drug_name', 'dosage', 'frequency', 'duration')
    search_fields = ('drug_name', 'medical_record__patient__name')
    list_filter = ('medical_record__patient__name',)

# Registering the Appointment model
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'appointment_date', 'reason', 'status')
    search_fields = ('patient__name', 'reason')
    list_filter = ('status', 'appointment_date')

# Registering the Billing model
@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medical_record', 'total_amount', 'paid_amount', 'payment_status', 'payment_date')
    search_fields = ('patient__name', 'transaction_reference')
    list_filter = ('payment_status', 'payment_date')

# Registering the HealthcareProvider model
@admin.register(HealthcareProvider)
class HealthcareProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'license_number')
    search_fields = ('name', 'license_number', 'email')

# Registering the LabTest model
@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'test_name', 'date_conducted', 'conducted_by')
    search_fields = ('test_name', 'medical_record__patient__name', 'conducted_by')
    list_filter = ('date_conducted',)

# Registering the BlockchainTransaction model
@admin.register(BlockchainTransaction)
class BlockchainTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_hash', 'related_record', 'timestamp')
    search_fields = ('transaction_hash', 'related_record')
    list_filter = ('timestamp',)
