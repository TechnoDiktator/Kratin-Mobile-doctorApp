from django.contrib import admin
from django.urls import path , include
from django.urls import path
from . import views

urlpatterns = [
    
    path("" , views.home , name = "home"),
    path('doctor/register/', views.doctor_register, name='doctor_register'),
    path('doctor/login/', views.doctor_login, name='doctor_login'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/logout/', views.doctor_logout, name='doctor_logout'),
    path('doctor/prescribe/', views.prescription, name='prescription'),

    path('patient/register/', views.patient_register, name='patient_register'),
    path('patient/login/', views.patient_login, name='patient_login'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/mark_medication/<int:prescription_id>/', views.mark_medication, name='mark_medication'),
    path('patient/logout/', views.patient_logout, name='patient_logout'),
]






