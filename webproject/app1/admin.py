
from django.contrib import admin
from .models import Patient, Doctor, Prescription

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Prescription)