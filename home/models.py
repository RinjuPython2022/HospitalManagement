from email.policy import default
from enum import unique
from random import choices
from django.db import models

# Create your models here.

class Departments(models.Model):
    dept_name=models.CharField(max_length=100)
    dept_description=models.TextField()
    dept_image=models.ImageField(upload_to='departments',default="")
    def __str__(self):
       return self.dept_name
class Doctors(models.Model):
    blood_choices=[
        ("O+","O+"),
        ("A+","A+"),
        ("B+","B+"),
        ("AB+","AB+")
        
    ]
    
    gender_choices=[
        ("Male","Male"),
        ("Female","Female")
    ]
    doc_name=models.CharField(max_length=255)
    doc_email=models.EmailField(unique=True,default="")#primary key for this model
    doc_phone=models.CharField(max_length=10,default="") 
    doc_address=models.TextField(default="")  
    gender=models.CharField(max_length=10,choices=gender_choices,default="")         
    #bitrhdate=models.DateField(default="")
    blood=models.CharField(max_length=10,default="",choices=blood_choices)
    #blood=models.CharField(max_length=10,default="")    
    doc_spec=models.CharField(max_length=255)
    dept_name=models.ForeignKey(Departments,on_delete=models.CASCADE)
    doc_image=models.ImageField(upload_to='doctors')
    def __str__(self):
        return 'Dr.' + self.doc_name +'(' + self.doc_spec + ')'
       
class Booking(models.Model):
    p_name=models.CharField(max_length=255)  
    p_phone=models.CharField(max_length=10)  
    p_email=models.EmailField()
    doc_name=models.ForeignKey(Doctors,on_delete=models.CASCADE)
    booking_date=models.DateField()
    booking_on=models.DateField(auto_now=True)
    p_token=models.IntegerField(editable=False,default="")    
    def __str__(self): 
        return self.p_name
    
class Contact(models.Model):
    cust_name=models.CharField(max_length=255)    
    cust_phone=models.CharField(max_length=10)
    cust_email=models.EmailField()
    cust_msg=models.TextField()
    def __str__(self):
        return self.cust_name

class Patient(models.Model):
        p_name=models.CharField(max_length=255)
        p_email=models.EmailField()
        username=models.CharField(max_length=255,unique=True)#primary key for this model
        gender=models.CharField(max_length=10)
        p_phone=models.CharField(max_length=10) 
        p_address=models.TextField()       
        bitrhdate=models.DateField()
        blood=models.CharField(max_length=10)
        
        def __str__(self):
            return self.p_name
        