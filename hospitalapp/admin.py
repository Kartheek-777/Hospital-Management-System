from django.contrib import admin
from .models import Department, Patient, Doctor, Appointment, Prescription, PatientQuery

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name', 'description')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'first_name', 'last_name', 'specialty', 'department', 'license_number', 'phone_number')
    search_fields = ('first_name', 'last_name', 'specialty', 'license_number', 'email')
    list_filter = ('specialty', 'department')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'medical_record_number', 'first_name', 'last_name', 'gender', 'age', 'phone_number', 'email')
    search_fields = ('medical_record_number', 'first_name', 'last_name', 'phone_number', 'email')
    list_filter = ('gender', 'blood_group')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'reason')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'disease', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'disease', 'prescription_text')

@admin.register(PatientQuery)
class PatientQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('patient_name', 'subject', 'query_text', 'admin_response')

admin.site.site_header = "Hospital Management Administration"
admin.site.site_title = "Hospital Portal Admin"
admin.site.index_title = "Welcome to Hospital Management Portal Admin"
