from django.contrib import admin

# Register your models here.
from .models import Patient, Doctor
admin.site.register(Patient)
admin.site.register(Doctor)

admin.site.site_header = "Hospital Management Admin"
admin.site.site_title = "Hospital Management Admin Portal"
admin.site.index_title = "Welcome to Hospital Management Portal"
admin.site.url = "hospitalapp"





