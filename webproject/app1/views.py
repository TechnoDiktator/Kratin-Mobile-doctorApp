from django.shortcuts import render
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from .models import User , Prescription , Patient , Doctor

# Create your views here.


from .models import Prescription


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
        return redirect('doctor_login')

    return render(request, 'app1/doctor_register.html')


def doctor_login(request):
    print("Trying to log in as doctor")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        print("Authenticating")
        user = authenticate(request, username=username, password=password)

        if user and user.is_doctor:
            print("user is a doctor")
            login(request, user)
            return render( request ,  'app1/doctor_dashboard.html'  )
        else:
            messages.error(request, 'Invalid credentials or you are not a doctor.')

    return render(request, 'app1/doctor_login.html')


@login_required(login_url='doctor_login')
def doctor_dashboard(request):
    if request.user.is_authenticated and request.user.is_doctor:
        doctor = request.user
        prescriptions = Prescription.objects.filter(doctor=doctor)

        context = {
            'prescriptions': prescriptions
        }
        return render(request, 'app1/doctor_dashboard.html', context)
    else:
        return redirect('doctor_login') 
    
    #patients = doctor.patient_set.all()
    #context = {'doctor': doctor, 'patients': patients}
    #return render(request, 'app1/doctor_dashboard.html', context)




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
        return redirect('patient_login')

    return render(request, 'app1/patient_register.html')


def patient_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        print(user.is_patient)
        print("trying to log in")
        if user and user.is_patient:
            print("user is patient")
            login(request, user)
            return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid credentials or you are not a patient.')

    return render(request, 'app1/patient_login.html')


@login_required(login_url='patient_login')
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

    return redirect('patient_dashboard')


def doctor_logout(request):
    logout(request)
    return redirect('doctor_login')


def patient_logout(request):
    logout(request)
    return redirect('patient_login')




###
#    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#    health_problem = models.CharField(max_length=100)
#    medication = models.CharField(max_length=100)
#    time_for_medication = models.TimeField()
#    from_date = models.DateField()
#    till_date = models.DateField()
###

def prescription(request):
    if request.method == 'POST':
        
        patient_name = request.POST.get('patient_name')
        health_problem = request.POST.get('health_problem')
        medication = request.POST.get('medication')
        instructions = request.POST.get('instructions')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        time_for_medication = request.POST.get('time_for_medication')

        prescription = Prescription(
            patient=patient_name,
            doctor = request.user,
            health_problem=health_problem,
            medication=medication,
            instructions=instructions,
            from_date=from_date,
            till_date=to_date,
            time_for_medication=time_for_medication
        )
        prescription.save()
        

        return redirect('doctor_dashboard')  

    return render(request, 'app1/prescription.html')


