from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)




class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    doctor_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.doctor_name


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    medications = models.ManyToManyField(Doctor, through='Prescription')

    def __str__(self):
        return self.name
    
    
    
    
class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    health_problem = models.CharField(max_length=100)
    medication = models.CharField(max_length=100)
    time_for_medication = models.TimeField()
    from_date = models.DateField()
    till_date = models.DateField()

    def __str__(self):
        return f'{self.patient.name} - {self.medication}'







# Create your models here.
