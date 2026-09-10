from django.urls import path
from . import views

urlpatterns = [
    # Public Homepage
    path('', views.home, name='home'),

    # Doctor Portal URLs
    path('doctor-login/', views.doctor_login, name='doctor_login'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/appointments/', views.view_appointments, name='view_appointments'),
    path('doctor/appointments/<int:appointment_id>/<str:status>/', views.update_appointment_status, name='update_appointment_status'),
    path('doctor/patients/', views.view_patients, name='view_patients'),
    path('doctor/add-prescription/', views.add_prescription, name='add_prescription'),
    path('doctor/add-prescription/<int:appointment_id>/', views.add_prescription, name='add_prescription_for_appointment'),
    path('doctor/logout/', views.doctor_logout, name='doctor_logout'),

    # Patient Portal URLs
    path('patient-register/', views.patient_register, name='patient_register'),
    path('patient-login/', views.patient_login, name='patient_login'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('view-doctors/', views.view_doctors, name='view_doctors'),
    path('view-prescriptions/', views.view_prescriptions, name='view_prescriptions'),
    path('patient-queries/', views.patient_queries, name='patient_queries'),
    path('patient-logout/', views.patient_logout, name='patient_logout'),

    # Admin Portal
    path('admin-login/', views.admin_login, name='admin_login'),
    path('respond-query/<int:query_id>/', views.respond_query, name='respond_query'),
]
