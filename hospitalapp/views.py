import random
import string
from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from .models import Department, Doctor, Patient, Appointment, Prescription, PatientQuery

def generate_mrn():
    """Generate a unique 8-character Medical Record Number."""
    while True:
        digits = ''.join(random.choices(string.digits, k=6))
        mrn = f"MRN-{digits}"
        if not Patient.objects.filter(medical_record_number=mrn).exists():
            return mrn

# ---------------- Public Views ----------------

def home(request):
    doctors_count = Doctor.objects.count()
    patients_count = Patient.objects.count()
    departments_count = Department.objects.count()
    appointments_count = Appointment.objects.count()
    doctors = Doctor.objects.all()[:6]
    departments = Department.objects.all()[:6]
    
    context = {
        'doctors_count': doctors_count,
        'patients_count': patients_count,
        'departments_count': departments_count,
        'appointments_count': appointments_count,
        'doctors': doctors,
        'departments': departments,
    }
    return render(request, "hospitalapp/home.html", context)

# ---------------- Doctor Portal Views ----------------

def doctor_login(request):
    if request.method == "POST":
        login_input = request.POST.get("doctor_id", "").strip()
        first_name = request.POST.get("first_name", "").strip()

        doctor = None
        # Try matching by license_number or doctor_id integer
        if login_input.isdigit():
            doctor = Doctor.objects.filter(doctor_id=int(login_input), first_name__iexact=first_name).first()
        if not doctor:
            doctor = Doctor.objects.filter(license_number__iexact=login_input, first_name__iexact=first_name).first()
        if not doctor:
            doctor = Doctor.objects.filter(email__iexact=login_input, first_name__iexact=first_name).first()

        if doctor:
            request.session["doctor_id"] = doctor.doctor_id
            request.session["doctor_license"] = doctor.license_number
            messages.success(request, f"Welcome back, Dr. {doctor.first_name}!")
            return redirect("doctor_dashboard")
        else:
            messages.error(request, "Invalid credentials. Please check your Doctor ID / License and First Name.")

    return render(request, "hospitalapp/doctor_login.html")

def get_logged_in_doctor(request):
    doctor_id = request.session.get("doctor_id")
    license_number = request.session.get("doctor_license")
    if doctor_id:
        try:
            return Doctor.objects.get(doctor_id=doctor_id)
        except Doctor.DoesNotExist:
            pass
    if license_number:
        try:
            return Doctor.objects.get(license_number=license_number)
        except Doctor.DoesNotExist:
            pass
    return None

def doctor_dashboard(request):
    doctor = get_logged_in_doctor(request)
    if not doctor:
        messages.error(request, "Please log in to access the Doctor Dashboard.")
        return redirect("doctor_login")

    today = date.today()
    all_appointments = Appointment.objects.filter(doctor=doctor)
    today_appointments = all_appointments.filter(date=today)
    pending_appointments = all_appointments.filter(status='Scheduled')
    completed_appointments = all_appointments.filter(status='Completed')
    patients_count = Patient.objects.filter(appointments__doctor=doctor).distinct().count()

    context = {
        'doctor': doctor,
        'total_appointments': all_appointments.count(),
        'today_appointments_count': today_appointments.count(),
        'pending_appointments_count': pending_appointments.count(),
        'completed_appointments_count': completed_appointments.count(),
        'patients_count': patients_count,
        'recent_appointments': today_appointments.order_by('time')[:5] or all_appointments.order_by('-date', '-time')[:5],
    }
    return render(request, "hospitalapp/doctor_dashboard.html", context)

def view_appointments(request):
    doctor = get_logged_in_doctor(request)
    if not doctor:
        messages.error(request, "Please log in to view appointments.")
        return redirect("doctor_login")

    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.filter(doctor=doctor)
    if status_filter:
        appointments = appointments.filter(status=status_filter)

    appointments = appointments.order_by('-date', 'time')

    return render(request, "hospitalapp/view_appointments.html", {
        "doctor": doctor,
        "appointments": appointments,
        "selected_status": status_filter,
    })

def update_appointment_status(request, appointment_id, status):
    doctor = get_logged_in_doctor(request)
    if not doctor:
        messages.error(request, "Please log in to manage appointments.")
        return redirect("doctor_login")

    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    if status in ['Confirmed', 'Completed', 'Cancelled']:
        appointment.status = status
        appointment.save()
        messages.success(request, f"Appointment status updated to {status}.")

    return redirect("view_appointments")

def view_patients(request):
    doctor = get_logged_in_doctor(request)
    if not doctor:
        messages.error(request, "Please log in first.")
        return redirect("doctor_login")

    search_query = request.GET.get('q', '').strip()
    patients = Patient.objects.filter(appointments__doctor=doctor).distinct()
    
    if search_query:
        patients = patients.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(medical_record_number__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    return render(request, "hospitalapp/view_patients.html", {
        "doctor": doctor,
        "patients": patients,
        "search_query": search_query,
    })

def add_prescription(request, appointment_id=None):
    doctor = get_logged_in_doctor(request)
    if not doctor:
        messages.error(request, "Please log in first.")
        return redirect("doctor_login")

    appointment = None
    target_patient = None
    if appointment_id:
        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
        target_patient = appointment.patient

    all_patients = Patient.objects.all().order_by('first_name')

    if request.method == "POST":
        patient_id = request.POST.get("patient_id")
        disease = request.POST.get("disease")
        prescription_text = request.POST.get("prescription_text")
        dosage = request.POST.get("dosage", "As directed")
        duration = request.POST.get("duration", "7 days")

        patient_obj = get_object_or_404(Patient, id=patient_id)
        prescription = Prescription.objects.create(
            doctor=doctor,
            doctor_name=f"Dr. {doctor.first_name} {doctor.last_name}",
            patient=patient_obj,
            appointment=appointment,
            disease=disease,
            prescription_text=prescription_text,
            dosage=dosage,
            duration=duration
        )

        if appointment:
            appointment.status = 'Completed'
            appointment.save()

        messages.success(request, f"Prescription successfully issued for {patient_obj.first_name} {patient_obj.last_name}!")
        return redirect("view_appointments")

    return render(request, "hospitalapp/add_prescription.html", {
        "doctor": doctor,
        "appointment": appointment,
        "target_patient": target_patient,
        "patients": all_patients,
    })

def doctor_logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect("doctor_login")

# ---------------- Patient Portal Views ----------------

def patient_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        dob = request.POST.get("date_of_birth")
        gender = request.POST.get("gender")
        blood_group = request.POST.get("blood_group")
        address = request.POST.get("address", "").strip()
        emergency_contact = request.POST.get("emergency_contact", "").strip()
        password = request.POST.get("password", "")

        mrn = generate_mrn()
        patient = Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            date_of_birth=dob if dob else None,
            gender=gender,
            blood_group=blood_group,
            address=address if address else "Not provided",
            emergency_contact=emergency_contact,
            medical_record_number=mrn,
            password=password
        )

        request.session['patient_id'] = patient.id
        messages.success(request, f"Registration successful! Your Medical Record Number (MRN) is: {mrn}. Please keep it for login.")
        return redirect("patient_dashboard")

    return render(request, "hospitalapp/patient_register.html")

def patient_login(request):
    if request.method == "POST":
        login_id = request.POST.get("login_id", "").strip() # MRN or Phone or Email
        phone_number = request.POST.get("phone_number", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        dob = request.POST.get("date_of_birth")

        patient = None
        # Flexible login matching
        if login_id:
            patient = Patient.objects.filter(
                Q(medical_record_number__iexact=login_id) |
                Q(phone_number__iexact=login_id) |
                Q(email__iexact=login_id)
            ).first()

        if not patient and first_name and phone_number:
            query = Patient.objects.filter(first_name__iexact=first_name, phone_number__exact=phone_number)
            if dob:
                query = query.filter(date_of_birth=dob)
            patient = query.first()

        if patient:
            request.session['patient_id'] = patient.id
            messages.success(request, f"Welcome back, {patient.first_name}!")
            return redirect("patient_dashboard")
        else:
            messages.error(request, "Invalid details. Please enter your valid MRN, Phone Number, or Register as a new patient.")

    return render(request, "hospitalapp/patient_login.html")

def get_logged_in_patient(request):
    patient_id = request.session.get('patient_id')
    if patient_id:
        try:
            return Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            pass
    return None

def patient_dashboard(request):
    patient = get_logged_in_patient(request)
    if not patient:
        messages.error(request, "Please log in to view your dashboard.")
        return redirect("patient_login")

    upcoming_appointments = Appointment.objects.filter(patient=patient, date__gte=date.today()).order_by('date', 'time')
    prescriptions = Prescription.objects.filter(patient=patient).order_by('-created_at')
    queries = PatientQuery.objects.filter(patient=patient).order_by('-created_at')

    context = {
        'patient': patient,
        'upcoming_appointments': upcoming_appointments,
        'upcoming_count': upcoming_appointments.count(),
        'prescriptions_count': prescriptions.count(),
        'queries_count': queries.count(),
        'recent_prescriptions': prescriptions[:3],
        'recent_queries': queries[:3],
    }
    return render(request, "hospitalapp/patient_dashboard.html", context)

def book_appointment(request):
    patient = get_logged_in_patient(request)
    if not patient:
        messages.error(request, "Please log in to book an appointment.")
        return redirect("patient_login")

    doctors = Doctor.objects.all()
    departments = Department.objects.all()
    msg = ""

    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        booking_date = request.POST.get("date")
        booking_time = request.POST.get("time")
        reason = request.POST.get("reason", "")

        doctor_obj = get_object_or_404(Doctor, doctor_id=doctor_id)
        Appointment.objects.create(
            patient=patient,
            doctor=doctor_obj,
            date=booking_date,
            time=booking_time,
            reason=reason,
            status='Scheduled'
        )
        messages.success(request, f"Appointment successfully booked with Dr. {doctor_obj.first_name} {doctor_obj.last_name} for {booking_date} at {booking_time}!")
        return redirect("patient_dashboard")

    return render(request, "hospitalapp/book_appointment.html", {
        "patient": patient,
        "doctors": doctors,
        "departments": departments,
        "today_date": date.today().strftime('%Y-%m-%d'),
    })

def cancel_appointment(request, appointment_id):
    patient = get_logged_in_patient(request)
    if not patient:
        messages.error(request, "Please log in first.")
        return redirect("patient_login")

    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)
    if appointment.status in ['Scheduled', 'Confirmed']:
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, "Your appointment has been cancelled.")

    return redirect("patient_dashboard")

def view_doctors(request):
    dept_id = request.GET.get('dept', '')
    search_q = request.GET.get('q', '').strip()

    doctors = Doctor.objects.all()
    departments = Department.objects.all()

    if dept_id:
        doctors = doctors.filter(department_id=dept_id)
    if search_q:
        doctors = doctors.filter(
            Q(first_name__icontains=search_q) |
            Q(last_name__icontains=search_q) |
            Q(specialty__icontains=search_q)
        )

    return render(request, "hospitalapp/view_doctors.html", {
        "doctors": doctors,
        "departments": departments,
        "selected_dept": dept_id,
        "search_q": search_q,
    })

def view_prescriptions(request):
    patient = get_logged_in_patient(request)
    if not patient:
        messages.error(request, "Please log in to view prescriptions.")
        return redirect("patient_login")

    prescriptions = Prescription.objects.filter(patient=patient).order_by('-created_at')
    return render(request, 'hospitalapp/view_prescriptions.html', {
        'patient': patient,
        'prescriptions': prescriptions
    })

def patient_queries(request):
    patient = get_logged_in_patient(request)
    if not patient:
        messages.error(request, "Please log in to submit queries.")
        return redirect("patient_login")

    if request.method == "POST":
        subject = request.POST.get("subject", "General Medical Inquiry")
        query_text = request.POST.get("query")

        PatientQuery.objects.create(
            patient=patient,
            patient_name=f"{patient.first_name} {patient.last_name}",
            subject=subject,
            query_text=query_text,
            status='Pending'
        )
        messages.success(request, "Your query has been successfully submitted! Our medical team will respond shortly.")
        return redirect("patient_queries")

    queries = PatientQuery.objects.filter(patient=patient).order_by('-created_at')
    return render(request, "hospitalapp/patient_queries.html", {
        "patient": patient,
        "queries": queries,
    })

def patient_logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect("patient_login")

# ---------------- Staff/Admin Support Views ----------------

def admin_login(request):
    return redirect('/admin/')

def respond_query(request, query_id):
    query = get_object_or_404(PatientQuery, id=query_id)
    if request.method == "POST":
        response_text = request.POST.get("admin_response")
        query.admin_response = response_text
        query.status = 'Responded'
        query.save()
        messages.success(request, "Response saved successfully.")
    return redirect("/admin/hospitalapp/patientquery/")
