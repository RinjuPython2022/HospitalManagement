from . import views
from django.urls import path


urlpatterns = [
    path('', views.home,name='home'),
    path('about/', views.about,name='about'),
    path('department/', views.department,name='department'),
    path('doctors/', views.doctors,name='doctors'),
    path('register/', views.register,name='register'),
    path('login/', views.loginpage,name='loginpage'),
    path('contact/', views.contact,name='contact'),
    path('homepage/', views.homepage,name='homepage'),
    path('profile/', views.profile,name='profile'),
    path('viewpage/', views.viewpage,name='viewpage'),
    path('booking/', views.booking,name='booking'),   
    path('logout/', views.logoutpage,name='logoutpage'),
    #path('patienthome/', views.patienthome,name='patienthome'),
    #path('patientprofile/', views.patientprofile,name='patientprofile'),    
    #path('doctorhome/', views.doctorhome,name='doctorhome'),
    #path('doctorprofile/', views.doctorprofile,name='doctorprofile'),
    #path('doctorview/', views.doctorview,name='doctorview'),
    
    
    
]