from django.contrib import admin

# Register your models here.
from .models import Booking, Contact, Departments, Doctors

admin.site.register(Departments)
admin.site.register(Doctors)
admin.site.register(Booking)
admin.site.register(Contact)