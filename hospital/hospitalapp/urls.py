from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),   # home page

    path('doctor-login/', views.doctor_login, name='doctor_login'),
    path('patient-login/', views.patient_login, name='patient_login'),
    path('admin-login/', views.admin_login, name='admin_login'),

    #--------------doctor dashboard urls-----------------
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/appointments/', views.view_appointments, name='view_appointments'),
    path('doctor/patients/', views.doctor_dashboard, name='view_patients'),
    path("view-patients/", views.view_patients, name="view_patients"),

    path('doctor/logout/', views.doctor_logout, name='doctor_logout'),

    #--------------patient dashboard urls-----------------
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('book-appointment/', views.book_appointment, name='book_appointment'), 
    path('view-doctors/', views.view_doctors, name='view_doctors'),
    path("view-prescriptions/", views.view_prescriptions, name="view_prescriptions"),
    path('patient-queries/', views.patient_queries, name='patient_queries'),
    #path('logout/', views.logout_view, name='logout'),


]
