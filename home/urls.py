from . import views
from django.urls import path


urlpatterns = [
    path('', views.home,name='home'),
    path('about/', views.about,name='about'),
    path('department/', views.department,name='department'),
    path('doctors/', views.doctors,name='doctors'),
    path('booking/', views.booking,name='booking'),
    path('contact/', views.contact,name='contact'),
    
    
]