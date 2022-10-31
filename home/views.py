from datetime import *
from unicodedata import name
from django.http import HttpResponse

from django.shortcuts import redirect, render
from django.contrib.auth.models import User,Group
from django.contrib.auth import login,authenticate,logout
from .forms import BookingForm
from django.template import loader
from django.contrib import messages
from .models import Departments, Doctors,Booking,Contact, Patient

# Create your views here.

def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html') 
def register(request):
    user="None"
    error=""
    if request.method=="POST":
        name=request.POST["name"]
        username=request.POST["username"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]
        phone=request.POST["phone"]
        email=request.POST["email"]
        gender=request.POST["gender"]
        address=request.POST["address"]
        blood=request.POST["blood"]
        birthdate=request.POST["birthdate"]
        try:
            if password1==password2:
                #error=user.objects.filter(username=username)
                if User.objects.filter(username=username).exists():
                    messages.info(request,'Username is already existing')
                    #return redirect('register')
                else:                    
                        #saving data except password into Patient table
                        Patient.objects.create(p_name=name,p_email=email,username=username,gender=gender,p_phone=phone,p_address=address,bitrhdate=birthdate,blood=blood)
                        #saving data including password to user table for authentication
                        user=User.objects.create_user(first_name=name,username=username,email=email,password=password1)
                        pat_group=Group.objects.get(name="patient")#geting the patient group
                        #pat_group.add_to_class(user)
                        pat_group.user_set.add(user)
                        user.save()
                        messages.info(request,'You have successfully registered')
                        return redirect('loginpage')                     
            else:
                messages.info(request,'Sorry.You have given different passwords')
                return redirect('register')
        except Exception as e:
            #raise e
            messages.info(request,'Something went wrong')
    dict={'error':error}           
    return render(request,'register.html')

def logoutpage(request):
    logout(request) 
    return redirect('loginpage')
    #return render(request,'logoutpage.html')
    
def loginpage(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        #try:
        if user is not None:            
            login(request,user)
            group=request.user.groups.all()[0].name
            #print("group",request.user.groups.all()[0].name)
            if group=="patient":
                return redirect('homepage')
                #return HttpResponse('You have logged in successfully')
            elif group=="doctor":
                return redirect('homepage')        
        #except Exception as e:
        #    raise e    
        
    return render(request,'login.html') 

#def patienthome(request):
def homepage(request):
    if not request.user.is_active:
        return redirect('loginpage')
    group=request.user.groups.all()[0].name
    if group=='patient':
        return render(request,'patienthome.html')
    elif group=='doctor':
        return render(request,'doctorhome.html')
    
#def patientprofile(request):
def profile(request):
    if not request.user.is_active:
        return redirect('loginpage')
    group=request.user.groups.all()[0].name
    if group=='patient':
        patient_details=Patient.objects.all().filter(username=request.user)
        d={'patient_details':patient_details}
        return render(request,'patientprofile.html',d) 
    elif group=='doctor':
        doctor_details=Doctors.objects.all().filter(doc_email=request.user)
        d={'doctor_details':doctor_details}
        return render(request,'doctorprofile.html',d)

#def patientview(request):
def viewpage(request):
    if not request.user.is_active:
        return redirect('loginpage')
    group=request.user.groups.all()[0].name
    today = datetime.now().date()
    print("today",today)
    if group=='patient':
        patient=Patient.objects.filter(username=request.user)        
        print("patient",patient)        
        if patient:# we check that the profile exists first
            pa_email = patient[0].p_email 
        print("pa_email",pa_email) 
        prev_appointment_details=Booking.objects.filter(p_email=pa_email,booking_date__lt=today).order_by('booking_date')
        today_appointment_details=Booking.objects.filter(p_email=pa_email,booking_date=today)
        coming_appointment_details=Booking.objects.filter(p_email=pa_email,booking_date__gt=today).order_by('booking_date')
        #data=Booking.objects.filter(p_email=request.user,booking_date=today)
        d={
            'today':today,'prev_appointment_details':prev_appointment_details,'today_appointment_details':today_appointment_details,'coming_appointment_details':coming_appointment_details
        }      
        
        return render(request,'patientview.html',d)
    
    elif group=='doctor':
        today = datetime.now().date()        
        doctor=Doctors.objects.get(doc_email=request.user)    
        #name=doctor.doc_name
        #print("name",name)
        #print("doctor",doctor)
        prev_booking_datails=Booking.objects.filter(doc_name=doctor,booking_date__lt=today).order_by('booking_date')
        today_booking_datails=Booking.objects.filter(doc_name=doctor,booking_date=today)
        coming_booking_datails=Booking.objects.filter(doc_name=doctor,booking_date__gt=today).order_by('booking_date')
        context={
                    'today':today,'today_booking_datails':today_booking_datails,'coming_booking_datails':coming_booking_datails,'prev_booking_datails':prev_booking_datails
                    }
        return render(request,'doctorview.html',context)  
def department(request):
    dept_count=Departments.objects.all().count() 
    first_dep=Departments.objects.all()[:4]    
    #last_dep=Departments.objects.all()[4:dept_count]
    #dict_dept={
    #    'department':Departments.objects.all()[3:5] 
    # } 
    dep={'first_dep':first_dep}
    #ldep={'last_dep':last_dep} 
    
    return render(request,'departments.html',dep)
    
def doctors(request):
    doc_count=Doctors.objects.all().count() 
    first_doc=Doctors.objects.all()[:3]    
    last_doc=Doctors.objects.all()[3:doc_count]
    dict_doc={
          'doctors':Doctors.objects.all(),'first_doc':first_doc,'last_doc':last_doc        
         }
    return render(request,'doctors.html',dict_doc)
def booking(request):
    if request.method=="POST":
        form=BookingForm(request.POST)
        if form.is_valid():
            name=request.POST.get("p_name")
            phone=request.POST.get("p_phone")
            #email=request.POST.get("p_email")
            doctor=request.POST.get("doc_name")
            date=request.POST.get("booking_date")
            #print("doctor",doctor)
            doctor_name=Doctors.objects.get(id=doctor)
            patient=Patient.objects.filter(username=request.user)
            #print("doctor_name.name",doctor_name.doc_name)
            #print("patient",patient)
            
            if patient:# we check that the profile exists first
                pa_email = patient[0].p_email 
            #print("pa_email",pa_email)    
            today = datetime.now().date()
            customer_data=0
            customer_data = Booking.objects.filter(booking_date=date,doc_name=doctor).count()
            
            booking=Booking(p_name=name,p_phone=phone,p_email=pa_email,doc_name=doctor_name,booking_date=date,p_token=customer_data+1)
            today_booking_datails=Booking.objects.filter(doc_name=doctor,booking_date=today)
            if customer_data<3:
                #form.save()
                booking.save()
                customer_data=customer_data+1                         
                
                context={
                    'customer_data':customer_data,'today':today,'doctor_name':doctor_name,'today_booking_datails':today_booking_datails
                    }
                return render(request,'confirm.html',context)
            else:
                messages.error(request,"Sorry,Today's appointment is full.Try another day.")
                return redirect('booking')
                #return render(request,'bookingfull.html')

    form=BookingForm()
    dict_form={'form':form}
    return render(request,'booking.html',dict_form)
def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        message=request.POST.get("message")
        contact=Contact(cust_name=name,cust_phone=phone,cust_email=email,cust_msg=message)
        contact.save()
        return render(request,'home.html')
    return render(request,'contact.html')


