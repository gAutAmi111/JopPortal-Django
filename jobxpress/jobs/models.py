from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
# job serachering 
class UserProfile(models.Model):
    userid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    type = (("Male", "Male"), ("Female", "Female"))
    gender = models.CharField(max_length=30, choices=type)
    dob = models.DateField(null=True, default=None)
    mobile = models.PositiveIntegerField()
    photo = models.ImageField(upload_to="images")
    
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, default=None
    )

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class Address(models.Model):
    userid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    address = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    pincode = models.PositiveIntegerField(
        validators=[MaxValueValidator(999999), MinValueValidator(100000)]
    )

    def __str__(self):
        return f"{self.address}, {self.city.name}, {self.city.country.name}"


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cname = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.cname if self.cname else self.user.username
    
def is_employer(self):
    return hasattr(self, 'employerprofile')

User.add_to_class('is_employer', is_employer)

    
class Company(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.CharField()

    job_type = models.CharField(max_length=20, choices=[
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ])

    requirements = models.TextField(help_text="Enter job requirements separated by commas", blank=True, null=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='INR')
    salary_frequency = models.CharField(
        max_length=20,
        choices=[('hourly', 'Hourly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')],
        default='yearly'
    )

    location = models.CharField(max_length=100, default=" ")
    email=models.EmailField()
    phone_number = PhoneNumberField(null=True, blank=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    about_company=models.CharField(max_length=400)
    website=models.CharField(max_length=100)
    photo = models.ImageField(upload_to='company_photos/', default='default.jpg')
    logo = models.ImageField(upload_to='company_logos/', default='default.jpg')


    def __str__(self):
        return f"{self.title} - {self.employer.cname}"
    

class Application(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)  # Or a JobSeekerProfile if you create one
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted')
    ], default='pending')
    email=models.EmailField(blank=True)

    # def __str__(self):
    #     return f"{self.applicant.username} -> {self.job.title}"
    

