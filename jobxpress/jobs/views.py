from django.shortcuts import render, redirect,get_object_or_404
from .models import UserProfile,Country,City,Address,EmployerProfile,Company,Application
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
import re
import ssl
import smtplib
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email
from django.utils import timezone
from django.conf import settings
from email.message import EmailMessage

def validate_email(email):
    try:
        django_validate_email(email)
    except ValidationError:
        raise ValidationError("Invalid email address.")


def index(request):
    allcompany = Company.objects.all()
    print(allcompany)
    return render(request, 'index.html',{'allcompany':allcompany})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

from django.shortcuts import render
from .models import Company

def job_listings(request):
    allcompany = Company.objects.all()
    context = {'allcompany': allcompany}
    return render(request, 'job-listings.html', context)

def job_details(request,id):
    company = Company.objects.get(id=id)
    print(company)
    similar_jobs = Company.objects.exclude(id=id)[:6] 
    context = {
        "company": company,
        "similar_jobs": similar_jobs,
        }
    return render(request, 'job-details.html',context)

from django.core.exceptions import ValidationError


def validate_password(password):
    if len(password) < 8 or len(password) > 128:
        raise ValidationError(
            "Password must be atleast 8 character long and less than 128"
        )

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    specialchars = "@$!%*?&"

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in specialchars:
            has_special = True

    if not has_upper:
        raise ValidationError("Password must contain at least one uppercase letter")

    if not has_lower:
        raise ValidationError("Password must contain at least one lowercase letter")

    if not has_digit:
        raise ValidationError("Password must contain at least one digit letter")

    if not has_special:
        raise ValidationError(
            "Password must contain at least one special char (e.g. @$!%*?&)"
        )

    commonpassword = ["password", "123456", "qwerty", "abc123"]
    if password in commonpassword:
        raise ValidationError("This password is too common. Please choose another one.")


from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import EmployerProfile, Company  # if needed

def signup(req, role):
    if req.method == "GET":
        return render(req, "register.html", {'role': role})

    # POST method logic
    uname = req.POST.get("uname")
    uemail = req.POST.get("uemail")
    upass = req.POST.get("upass")
    ucpass = req.POST.get("ucpass")
    cname = req.POST.get("cname") if role == 'recruiter' else None

    context = {'role': role}

    # Username uniqueness check
    if User.objects.filter(username=uname).exists():
        context["errmsg"] = "Username already exists. Please choose another."
        return render(req, "register.html", context)

    # Password validation
    try:
        validate_password(upass)
    except ValidationError as e:
        context["errmsg"] = str(e)
        return render(req, "register.html", context)

    if upass != ucpass:
        context["errmsg"] = "Password and Confirm password must be same"
        return render(req, "register.html", context)

    if uname == upass:
        context["errmsg"] = "Password should not be same as username"
        return render(req, "register.html", context)

    try:
        # Create user
        userdata = User.objects.create_user(
            username=uname,
            email=uemail,
            password=upass
        )

        # If recruiter, create EmployerProfile and assign cname
        if role == 'recruiter':
            employerprofile = EmployerProfile.objects.create(user=userdata,cname=cname)
            return redirect("signin")
        else:    
            return redirect("signin")

    except Exception as e:
        context["errmsg"] = f"Error: {str(e)}"
        return render(req, "register.html", context)


from django.contrib.auth import authenticate, login, logout

def signin(req):
    if req.method == "GET":
        print(req.method)
        return render(req, "login.html")
    else:
        uname = req.POST.get("uname")
        uemail = req.POST.get("uemail")
        upass = req.POST["upass"]
        print(uname, uemail, upass)
        
        userdata = authenticate(req, username=uname, password=upass)
        print(userdata)  # if matched with user then it show its id
        
        if userdata is not None:
            login(req, userdata)
            return redirect("index")
        else:
            context = {}
            context["errmsg"] = "Invalid email or password"
            return render(req, "login.html", context)

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=username, email=email)
            request.session['reset_user_id'] = user.id  # Store user in session
            return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or email.')
    return render(request, 'forgot_password.html')


def reset_password(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, 'Unauthorized access.')
        return redirect('forgot_password')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Password reset successful. Please log in.')
        request.session.flush()   
        return redirect('signin')  
    
    return render(request, 'reset_password.html')




def userlogout(req):
    logout(req)
    return redirect("/")

from django.shortcuts import render, redirect
from .models import Company
from django.contrib.auth.decorators import login_required
from phonenumber_field.phonenumber import to_python as parse_phone

@login_required
def add_job(request):
    if request.method == 'POST':
        employer = request.user.employerprofile  # assuming 1-to-1 with user

        Company.objects.create(
            employer=employer,
            title=request.POST['title'],
            description=request.POST['description'],
            job_type=request.POST['job_type'],
            salary_min=request.POST.get('salary_min') or None,
            salary_max=request.POST.get('salary_max') or None,
            currency=request.POST['currency'],
            salary_frequency=request.POST['salary_frequency'],
            location=request.POST['location'],
            email=request.POST['email'],
            phone_number=parse_phone(request.POST.get('phone_number')),
            about_company=request.POST['about_company'],
            website=request.POST['website'],
            photo=request.FILES.get('photo'),
            logo=request.FILES.get('logo'),
        )
        return redirect('job_listings')  

    return render(request, 'company_form.html')

def searchbytitle(req):
    query = req.GET.get("q", "")  
    if query:
        allcompany = Company.objects.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )
        if not allcompany.exists():
            messages.error(req, "No result found!!")
    else:
        allcompany = Company.objects.all()

    context = {"allcompany": allcompany,"query": query}
    return render(req, "index.html", context)


def applyform(request, id):
    username = request.user
    company = get_object_or_404(Company, id=id)

    if request.method == "GET":
        return render(request, "apply_form.html", {
            "username": username,
            "company": company,
        })

    # POST
    resume = request.POST.get('resume', '').strip()
    cover_letter = request.POST.get('cover_letter', '').strip()
    email = request.POST.get('email', '').strip()

    print(resume, cover_letter, email)

    # 1) Validate email
    try:
        validate_email(email)
    except ValidationError as e:
        messages.error(request, e.messages[0])
        return redirect('applyform', id=company.id)

    # 3) Create Application
    try:
        application = Application.objects.create(
            applicant=request.user,
            company=company,
            resume=resume,
            cover_letter=cover_letter,
            applied_at=timezone.now().date(),
            email=email,
        )
    except Exception as e:
        messages.error(request, f"Error creating application: {e}")
        return render(request, "apply_form.html", {
            "company": company,
            "username": request.user,
            "error": e.messages[0],
        })

    # 4) Send email
    sender = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    receiver = email

    msg = EmailMessage()
    msg.set_content(
        f"Dear {username} 🌟,\n\n"
        f"Woohoo! 🎉 Your application for the {company.title} position at {company.employer.cname} has been successfully submitted! \n\n"
        f"We’ve received your resume and cover letter, and our team is excited to review your materials. "
        f"We’ll reach out soon if your profile is a great match for this opportunity! 🚀\n\n"
        f"📋 Your Application Snapshot:\n"
        f"🏢 Company: {company.employer.cname}\n"
        f"💼 Position: {company.title}\n"
        f"📅 Application Date: {timezone.now().date()}\n"
        f"📧 Email: {email}\n\n"
        f"Thank you for choosing to explore a future with JobXpress! 🙌 We’re thrilled to have you on this journey "
        f"and will be in touch with updates soon. Stay awesome! 😊\n\n"
        f"Warm regards,\n"
        f"The JobXpress Talent Team  🤝"
    )
    msg["Subject"] = f"🎉 Application Confirmed! - {company.title} at {company.employer.cname}"
    msg["From"] = sender
    msg["To"] = receiver

    context = ssl._create_unverified_context()

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(sender, password)
            server.send_message(msg)
        return redirect("index")
    except Exception as e:
        messages.error(request, f"❌ Failed to send email: {e}")
        return render(request, 'apply_form.html', {
            "company": company,
            "username": request.user,
        })
        
        
    