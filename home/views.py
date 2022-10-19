from datetime import *
from django.shortcuts import render

from .forms import BookingForm
from django.template import loader

from .models import Departments, Doctors,Booking,Contact

# Create your views here.

def home(request):
        return render(request,'home.html')
def about(request):
        return render(request,'about.html')
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
            email=request.POST.get("p_email")
            doctor=request.POST.get("doc_name")
            date=request.POST.get("booking_date")
            print("doctor",doctor)
            doctor_name=Doctors.objects.get(id=doctor)
            print("doctor_name.name",doctor_name.doc_name)
            print("doctor_name",doctor_name)
            today = datetime.now().date()
            customer_data=0
            customer_data = Booking.objects.filter(booking_date=today,doc_name=doctor).count()
            mydata = Booking.objects.filter(p_name=name,doc_name=doctor,booking_date=today) 
            booking=Booking(p_name=name,p_phone=phone,p_email=email,doc_name=doctor_name,booking_date=date,p_token=customer_data+1)
            booking_datails=Booking.objects.all().values()
            if customer_data<5:
                #form.save()
                booking.save()
                customer_data=customer_data+1                         
                
                context={
                    'customer_data':customer_data,'mydata':mydata,'booking_datails':booking_datails
                    }
                return render(request,'confirm.html',context)
            else:
                
                return render(request,'bookingfull.html')

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


