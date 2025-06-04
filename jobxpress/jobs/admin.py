from django.contrib import admin
from .models import UserProfile,Country,City,Address,EmployerProfile,Company,Application

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["userid", "gender", "dob", "mobile", "photo"]
    
admin.site.register(UserProfile, UserProfileAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ["name"]

admin.site.register(Country, CountryAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "country"]
    
admin.site.register(City, CityAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ["userid", "address","city","country","pincode"]
    
admin.site.register(Address, AddressAdmin)


class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "cname"]
    
admin.site.register(EmployerProfile, EmployerProfileAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["employer", "title","description","job_type","salary_min","salary_max","currency","salary_frequency","location","email","phone_number","created_at","about_company","website","photo","logo"]
    
admin.site.register(Company, CompanyAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["company","applicant","resume","cover_letter","applied_at","status","email"]
    
admin.site.register(Application, ApplicationAdmin)
