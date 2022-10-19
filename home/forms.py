from datetime import date
from django import forms
from django import forms
from .models import Booking, Contact
class DateInput(forms.DateInput):
    input_type='date'
class BookingForm(forms.ModelForm):
    
     class Meta:
         model=Booking
         fields='__all__'
         labels={
             'p_name':'Name',
             'p_phone':'Phone',
             'p_email':'Email',
             'doc_name':'Doctor',
             'booking_date':'Booking Date'
         }
         widgets={'booking_date':DateInput()}
        
#class ContactForm(forms.ModelForm):
#    class Meta:
        
#        model=Contact
#        fields='__all__'