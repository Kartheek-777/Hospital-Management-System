from datetime import date, timedelta, time
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hospitalapp.models import Department, Doctor, Patient, Appointment, Prescription, PatientQuery

class Command(BaseCommand):
    help = 'Seeds the database with initial sample departments, doctors, patients, appointments, and prescriptions.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # 1. Create Superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@hospital.com', 'adminpass')
            self.stdout.write(self.style.SUCCESS('Created superuser (Username: admin, Password: adminpass)'))

        # 2. Create Departments
        departments_data = [
            ('Cardiology', 'Heart, blood vessels, and cardiovascular health care.', 'fa-heartbeat'),
            ('Neurology', 'Diagnosis and treatment of brain and nervous system disorders.', 'fa-brain'),
            ('Pediatrics', 'Comprehensive healthcare for infants, children, and adolescents.', 'fa-baby'),
            ('Orthopedics', 'Bone, joint, ligament, and musculoskeletal treatments.', 'fa-bone'),
            ('General Medicine', 'Primary healthcare, routine physicals, and preventative medicine.', 'fa-user-md'),
            ('Dermatology', 'Skin, hair, and nail clinical care and treatments.', 'fa-allergies'),
        ]

        depts = {}
        for name, desc, icon in departments_data:
            dept, created = Department.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'icon': icon}
            )
            depts[name] = dept

        # 3. Create Doctors
        doctors_data = [
            {
                'doctor_id': 101,
                'first_name': 'Sarah',
                'last_name': 'Jenkins',
                'specialty': 'Cardiologist',
                'department': depts['Cardiology'],
                'license_number': 'DOC1001',
                'email': 'sarah.jenkins@hospital.com',
                'phone_number': '+1 (555) 234-5678',
                'qualification': 'MD, FACC Cardiology',
                'experience_years': 12,
                'consultation_fee': 800.00,
                'available_days': 'Mon, Wed, Fri',
                'available_time': '09:00 AM - 02:00 PM',
            },
            {
                'doctor_id': 102,
                'first_name': 'Robert',
                'last_name': 'Chen',
                'specialty': 'Neurologist',
                'department': depts['Neurology'],
                'license_number': 'DOC1002',
                'email': 'robert.chen@hospital.com',
                'phone_number': '+1 (555) 345-6789',
                'qualification': 'MD, PhD Neurology',
                'experience_years': 15,
                'consultation_fee': 1000.00,
                'available_days': 'Tue, Thu, Sat',
                'available_time': '10:00 AM - 04:00 PM',
            },
            {
                'doctor_id': 103,
                'first_name': 'Emily',
                'last_name': 'Taylor',
                'specialty': 'Pediatrician',
                'department': depts['Pediatrics'],
                'license_number': 'DOC1003',
                'email': 'emily.taylor@hospital.com',
                'phone_number': '+1 (555) 456-7890',
                'qualification': 'MD Pediatrics',
                'experience_years': 8,
                'consultation_fee': 600.00,
                'available_days': 'Mon - Fri',
                'available_time': '08:30 AM - 01:30 PM',
            },
            {
                'doctor_id': 104,
                'first_name': 'Michael',
                'last_name': 'Adams',
                'specialty': 'Orthopedic Surgeon',
                'department': depts['Orthopedics'],
                'license_number': 'DOC1004',
                'email': 'michael.adams@hospital.com',
                'phone_number': '+1 (555) 567-8901',
                'qualification': 'MS, FRCS Orthopedics',
                'experience_years': 14,
                'consultation_fee': 900.00,
                'available_days': 'Mon, Tue, Thu',
                'available_time': '11:00 AM - 05:00 PM',
            },
            {
                'doctor_id': 105,
                'first_name': 'Lisa',
                'last_name': 'Gupta',
                'specialty': 'General Physician',
                'department': depts['General Medicine'],
                'license_number': 'DOC1005',
                'email': 'lisa.gupta@hospital.com',
                'phone_number': '+1 (555) 678-9012',
                'qualification': 'MBBS, MD Internal Medicine',
                'experience_years': 10,
                'consultation_fee': 500.00,
                'available_days': 'Mon - Sat',
                'available_time': '09:00 AM - 05:00 PM',
            },
        ]

        doctors = []
        for d_data in doctors_data:
            doc, created = Doctor.objects.get_or_create(
                doctor_id=d_data['doctor_id'],
                defaults=d_data
            )
            if not created:
                for k, v in d_data.items():
                    setattr(doc, k, v)
                doc.save()
            doctors.append(doc)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(doctors)} doctors."))

        # 4. Create Patients
        patients_data = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': date(1988, 5, 12),
                'age': 38,
                'gender': 'Male',
                'blood_group': 'O+',
                'address': '124 Pine Street, Cityville',
                'phone_number': '9876543210',
                'email': 'john.doe@example.com',
                'emergency_contact': '+1 555-999-1111',
                'medical_record_number': 'MRN-100201',
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'date_of_birth': date(1992, 8, 25),
                'age': 34,
                'gender': 'Female',
                'blood_group': 'A+',
                'address': '456 Maple Avenue, Townsville',
                'phone_number': '9876543211',
                'email': 'jane.smith@example.com',
                'emergency_contact': '+1 555-999-2222',
                'medical_record_number': 'MRN-100202',
            },
            {
                'first_name': 'David',
                'last_name': 'Wilson',
                'date_of_birth': date(1975, 11, 3),
                'age': 51,
                'gender': 'Male',
                'blood_group': 'B+',
                'address': '789 Oak Lane, Metro City',
                'phone_number': '9876543212',
                'email': 'david.wilson@example.com',
                'emergency_contact': '+1 555-999-3333',
                'medical_record_number': 'MRN-100203',
            },
        ]

        patients = []
        for p_data in patients_data:
            pat, created = Patient.objects.get_or_create(
                medical_record_number=p_data['medical_record_number'],
                defaults=p_data
            )
            patients.append(pat)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(patients)} patients."))

        # 5. Create Appointments
        today = date.today()
        appointments_data = [
            {
                'patient': patients[0],
                'doctor': doctors[0], # Dr. Sarah Jenkins
                'date': today + timedelta(days=1),
                'time': time(10, 0),
                'status': 'Scheduled',
                'reason': 'Routine cardiovascular checkup and ECG review.',
            },
            {
                'patient': patients[1],
                'doctor': doctors[4], # Dr. Lisa Gupta
                'date': today,
                'time': time(11, 30),
                'status': 'Confirmed',
                'reason': 'Seasonal flu, fever and throat pain.',
            },
            {
                'patient': patients[2],
                'doctor': doctors[1], # Dr. Robert Chen
                'date': today - timedelta(days=2),
                'time': time(14, 0),
                'status': 'Completed',
                'reason': 'Persistent migraine and sleep disturbance.',
            },
            {
                'patient': patients[0],
                'doctor': doctors[3], # Dr. Michael Adams
                'date': today - timedelta(days=5),
                'time': time(15, 30),
                'status': 'Completed',
                'reason': 'Knee joint pain after workout.',
            },
        ]

        created_appointments = []
        for app_data in appointments_data:
            app, created = Appointment.objects.get_or_create(
                patient=app_data['patient'],
                doctor=app_data['doctor'],
                date=app_data['date'],
                time=app_data['time'],
                defaults=app_data
            )
            created_appointments.append(app)

        # 6. Create Prescriptions
        Prescription.objects.get_or_create(
            patient=patients[2],
            disease='Migraine & Sleep Disruption',
            defaults={
                'doctor': doctors[1],
                'doctor_name': 'Dr. Robert Chen',
                'appointment': created_appointments[2],
                'prescription_text': '1. Sumatriptan 50mg - 1 tablet as needed for severe headache\n2. Melatonin 3mg - 1 tablet before bedtime\n3. Stay hydrated and avoid screen glare.',
                'dosage': 'As directed above',
                'duration': '14 days'
            }
        )

        Prescription.objects.get_or_create(
            patient=patients[0],
            disease='Knee Ligament Strain',
            defaults={
                'doctor': doctors[3],
                'doctor_name': 'Dr. Michael Adams',
                'appointment': created_appointments[3],
                'prescription_text': '1. Ibuprofen 400mg - 1 tablet twice daily after meals\n2. Apply cold compress for 15 mins 3x daily\n3. Knee sleeve support during walking.',
                'dosage': 'Twice Daily',
                'duration': '7 days'
            }
        )

        # 7. Create Patient Queries
        PatientQuery.objects.get_or_create(
            patient=patients[1],
            subject='Online Appointment Rescheduling Query',
            defaults={
                'patient_name': 'Jane Smith',
                'query_text': 'Hi, can I change my appointment time with Dr. Lisa Gupta to 2:00 PM if available?',
                'status': 'Responded',
                'admin_response': 'Dear Jane, your request is noted. Please check your dashboard for confirmed timings.'
            }
        )

        PatientQuery.objects.get_or_create(
            patient=patients[0],
            subject='Lab Test Preparation Inquiry',
            defaults={
                'patient_name': 'John Doe',
                'query_text': 'Do I need to fast before my scheduled blood checkup tomorrow?',
                'status': 'Pending',
                'admin_response': ''
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded Hospital database with sample records!'))
