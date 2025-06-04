from django.urls import path
from . import views 
from .views import signin


urlpatterns = [
    path("",views.index,name="index"),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path("signin/", views.signin, name="signin"),    
    path('signup/<str:role>/', views.signup, name='signup'),
    path("userlogout/", views.userlogout, name="userlogout"),
    path('jobs/', views.job_listings, name='job_listings'),
    path('jobs/details/<int:id>/', views.job_details, name='job_details'),
    path('add_job/', views.add_job, name='add_job'),
    path('searchbytitle/', views.searchbytitle, name='searchbytitle'),
    path('applyform/<int:id>/', views.applyform, name='applyform'),
    path('jobs/<int:id>/', views.job_details, name='job_details'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),


]