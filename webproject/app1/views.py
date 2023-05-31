from django.shortcuts import render
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

# Create your views here.



def home(request):
    context = {}
    return render(request , "app1/home.html"  , context)




def doctor_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        doctor_name = request.POST['doctor_name']
        email = request.POST['email']

        user = User.objects.create_user(username=username, password=password, is_doctor=True)
        Doctor.objects.create(user=user, doctor_name=doctor_name, email=email)

        messages.success(request, 'Doctor registered successfully!')
        return redirect('app1/doctor_login')

    return render(request, 'app1/doctor_register.html')


def doctor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user and user.is_doctor:
            login(request, user)
            return redirect('app1/doctor_dashboard')
        else:
            messages.error(request, 'Invalid credentials or you are not a doctor.')

    return render(request, 'app1/doctor_login.html')


@login_required(login_url='app1/doctor_login')
def doctor_dashboard(request):
    doctor = request.user.doctor
    patients = doctor.patient_set.all()
    context = {'doctor': doctor, 'patients': patients}
    return render(request, 'app1/doctor_dashboard.html', context)


def patient_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        email = request.POST['email']

        user = User.objects.create_user(username=username, password=password, is_patient=True)
        Patient.objects.create(user=user, name=name, age=age, gender=gender, email=email)

        messages.success(request, 'Patient registered successfully!')
        return redirect('app1/patient_login')

    return render(request, 'patient_register.html')


def patient_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user and user.is_patient:
            login(request, user)
            return redirect('app1/patient_dashboard')
        else:
            messages.error(request, 'Invalid credentials or you are not a patient.')

    return render(request, 'app1/patient_login.html')


@login_required(login_url='app1/patient_login')
def patient_dashboard(request):
    patient = request.user.patient
    medications = patient.prescription_set.all()
    today = date.today()
    calendar = []
    
    
    
    
    for prescription in medications:
        remaining_days = (prescription.till_date - today).days
        if remaining_days >= 0:
            status = 'Taken'
            if today > prescription.till_date:
                status = 'Missed'
            elif today == prescription.till_date:
                status = 'Today'
            calendar.append({'prescription': prescription, 'status': status})

    context = {'patient': patient, 'calendar': calendar}
    return render(request, 'app1/patient_dashboard.html', context)


def mark_medication(request, prescription_id):
    if request.method == 'POST':
        prescription = Prescription.objects.get(pk=prescription_id)
        patient = prescription.patient
        today = date.today()
        
        if prescription.from_date <= today <= prescription.till_date:
            prescription.status = 'Taken'
            prescription.save()
            messages.success(request, 'Medication marked as taken!')
        else:
            messages.error(request, 'Cannot mark medication outside the prescribed dates.')

    return redirect('app1/patient_dashboard')


def doctor_logout(request):
    logout(request)
    return redirect('app1/doctor_login')


def patient_logout(request):
    logout(request)
    return redirect('app1/patient_login')




