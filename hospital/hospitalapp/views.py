from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render
from django.contrib import messages
from .models import Doctor, Patient, PatientQuery, Prescription, Appointment


# Create your views here.
def home(request):
    return render(request, "hospitalapp/home.html")


# from django.shortcuts import render, redirect
# from .models import Doctor


def doctor_login(request):
    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        first_name = request.POST.get("first_name")

        try:
            doctor = Doctor.objects.get(doctor_id=doctor_id, first_name=first_name)
            request.session["doctor_id"] = doctor.doctor_id
            return redirect("doctor_dashboard")

        except Doctor.DoesNotExist:
            return render(request, "doctor_login.html", {"error": "Invalid Doctor ID or Name"})

    return render(request, "doctor_login.html")


def patient_login(request):
    error = ""
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        phone_number = request.POST.get("phone_number")
        dob = request.POST.get("date_of_birth")
        mrn = request.POST.get("medical_record_number")

        try:
            patient = Patient.objects.get(
                first_name=first_name,
                phone_number=phone_number,
                date_of_birth=dob,
                medical_record_number=mrn
            )
            # Save patient ID in session
            request.session['patient_id'] = patient.id
            # Redirect to patient dashboard
            return redirect("patient_dashboard")
        except Patient.DoesNotExist:
            error = "Invalid credentials. Please check your details."

    return render(request, "hospitalapp/patient_login.html", {"error": error})


def admin_login(request):
    return render(request, "admin_login.html")
    

#--------------doctor dashboard views-----------------
def doctor_dashboard(request):
    license_number = request.session.get("doctor_license")
    if not license_number:
        messages.error(request, "Please login first")
        return redirect("doctor_login")

    doctor = Doctor.objects.get(license_number=license_number)
    return render(request, "hospitalapp/doctor_dashboard.html", {"doctor": doctor})


def view_appointments(request):
    license_number = request.session.get("doctor_license")
    if not license_number:
        messages.error(request, "Please login first")
        return redirect("doctor_login")

    doctor = Doctor.objects.get(license_number=license_number)

    # Use correct field names
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date', 'time')

    return render(request, "hospitalapp/view_appointments.html", {
        "doctor": doctor,
        "appointments": appointments
    })

def view_patients(request):
    license_number = request.session.get("doctor_license")
    if not license_number:
        messages.error(request, "Please login first")
        return redirect("doctor_login")

    doctor = Doctor.objects.get(license_number=license_number)

    # Get all patients who have appointments with this doctor
    patients = Patient.objects.filter(appointment__doctor=doctor).distinct()

    return render(request, "hospitalapp/view_patients.html", {
        "doctor": doctor,
        "patients": patients
    })

#--------------patient dashboard views-----------------
def patient_dashboard(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('hospitalapp/patient_login')  # Not logged in

    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, "hospitalapp/patient_dashboard.html", {"patient": patient})




def book_appointment(request):
    doctors = Doctor.objects.all()
    msg = ""
    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        date = request.POST.get("date")
        time = request.POST.get("time")
        patient_id = request.session.get("patient_id")

        if patient_id:
            patient_obj = Patient.objects.get(id=patient_id)
            doctor_obj = Doctor.objects.get(id=doctor_id)

            Appointment.objects.create(
                patient=patient_obj,
                doctor=doctor_obj,
                date=date,
                time=time
            )
            msg = "Appointment booked successfully!"

    return render(request, "hospitalapp/book_appointment.html", {"doctors": doctors, "msg": msg})




def view_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, "hospitalapp/view_doctors.html", {"doctors": doctors})


def view_prescriptions(request):
    # If you have patient session
    patient_id = request.session.get('patient_id')
    prescriptions = Prescription.objects.filter(patient_id=patient_id)
    return render(request, 'hospitalapp/view_prescriptions.html', {'prescriptions': prescriptions})

def patient_queries(request):
    if request.method == "POST":
        query_text = request.POST.get("query")

        patient_id = request.session.get("patient_id")
        patient = Patient.objects.get(id=patient_id)

        PatientQuery.objects.create(
            patient_name=patient.first_name,
            query_text=query_text
        )

        messages.success(request, "Your query has been successfully submitted!")
        return redirect("patient_dashboard")  # FIX redirect name

    return render(request, "hospitalapp/patient_queries.html")



def doctor_logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect("doctor_login")
                    
