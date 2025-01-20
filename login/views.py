
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
import csv
from django.http import HttpResponse
import io
import requests
from .models import ExcelFile
from django.http import HttpResponse

# views.py

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

def test_session(request):
    if 'visited' in request.session:
        request.session['visited'] += 1
    else:
        request.session['visited'] = 1
    return HttpResponse(f"Number of visits: {request.session['visited']}")

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .models import GoogleSheet  # Assuming you have a GoogleSheet model
import csv



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import gspread
from oauth2client.service_account import ServiceAccountCredentials




from django.shortcuts import render, redirect
from .forms import ExcelFileForm

from django.shortcuts import render, redirect


from django.shortcuts import render, redirect
from .forms import ExcelFileForm


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from login.models import ParticipantConsent  # Adjust this import based on your app structure
import random

def signup(request):
    if request.method == 'POST':
        # Basic signup fields
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

    

        # Check if all required fields are filled
        if not all([username, email, password1, password2]):
            messages.error(request, "All required fields must be filled.")
            return render(request, 'signup.html')

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return render(request, 'signup.html')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'signup.html')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        try:
            # Store the additional health-related information in the session
            request.session['username'] = username
            request.session['email'] = email
            request.session['password1'] = password1

            # Generate and send OTP
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp

            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                'vipulkhosya00007@gmail.com',  # Replace with your sending email
                [email],
                fail_silently=False,
            )
            return redirect('verify_otp')  # Redirect to OTP verification
        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")
            return render(request, 'signup.html')

    return render(request, 'signup.html')

from django.contrib.auth.models import User
from .models import UserProfile  # Import the UserProfile model
from django.http import JsonResponse

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')

        if otp == str(request.session.get('otp')):
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                return JsonResponse({'success': False, 'message': 'Passwords do not match'})

            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username is already taken'})
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email is already registered'})

            try:
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password1)
                
                # Create the corresponding UserProfile entry
                UserProfile.objects.create(user=user)

                return JsonResponse({'success': True, 'message': 'Signup successful'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error creating user: {str(e)}'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid OTP. Please retry.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import random
import json

def send_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username')

            # Validate email format
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'success': False, 'message': 'Invalid email address'})

            # Check if the email or username is already registered
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email is already registered'})

            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username is already taken'})

            # Generate and save OTP
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['username'] = username

            # Send OTP via email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                'vipulkhosya00007@gmail.com',  # Replace with your sending email
                [email],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': 'OTP sent successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid request format'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import VisitorCount

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Check if visitor count is already incremented for the user
            if not hasattr(user, 'is_visitor_counted') or not user.is_visitor_counted:
                # Increment visitor count using the model
                visitor_count = VisitorCount.increment()  # Increment visitor count
                user.is_visitor_counted = True  # Mark the user as having counted the visit
                user.save()
            
            return redirect('subject_page')  # Redirect to subject page if login is successful
        else:
            messages.error(request, 'Invalid username or password')  # Show error message on invalid login
    
    return render(request, 'login.html')  # Render the login template


def LogoutPage(request):
    logout(request)
    return redirect('welcome')



# views.py


def get_encoding(file_path):
    """Detect the encoding of the file."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']



def ContactPage(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data if you have a model
            return redirect('contact_success')  # Redirect to success page
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')
def privacy_view(request):
    return render(request, 'privacy.html')
def term_view(request):
    return render(request, 'term.html')
def AboutPage(request):
    return render(request, 'about.html')
# views.py



def welcome_about(request):
    return render(request, 'welcome_about.html')

def welcome_contact(request):
    return render(request, 'welcome_contact.html')

from django.shortcuts import render
from .models import GoogleSheet

from django.contrib.auth.decorators import login_required

@login_required  # Ensure the user is logged in
def view_files(request):
    if request.user.is_superuser:
        # Superuser sees all files
        google_sheets = GoogleSheet.objects.all().select_related('user')  # Prefetch user data if needed
    else:
        # Normal user sees only their files
        google_sheets = GoogleSheet.objects.filter(user=request.user)
    
    return render(request, 'view_files.html', {'google_sheets': google_sheets})


from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import send_mail
import random
import string

User = get_user_model()

from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    # You don't need to override form_valid unless adding extra custom logic


    def send_new_password_email(self, user, new_password):
        subject = 'Your New Password'
        message = f'Hi {user.username},\n\nYour new password is: {new_password}\n\nPlease use this password to log in and change it once you are logged in.'
        from_email = 'your_email@example.com'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # If the password has been generated, add it to the context for the template
        if 'new_password' in self.kwargs:
            context['new_password'] = self.kwargs['new_password']
        return context

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # If the password has been generated, add it to the context for the template
        if 'new_password' in self.kwargs:
            context['new_password'] = self.kwargs['new_password']
        return context




from django.shortcuts import render, redirect
from .forms import ContactForm

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ContactMessage
from .forms import ContactForm



def contact_success_view(request):
    return render(request, 'contact_success.html')



from django.conf import settings
from django.shortcuts import redirect, HttpResponse
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.auth
import gspread
import os
import pickle





# views.py
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from django.shortcuts import render
from .forms import ContactForm

def contact_view(request):
    success_message = None

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = "Thank you! Your message has been sent."
            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, 'success': success_message})

def welcome_contact_view(request):
    success_message = None

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = "Thank you! Your message has been sent."
            form = ContactForm()  # Reset the form after submission
    else:
        form = ContactForm()

    return render(request, 'welcome_contact.html', {'form': form, 'success': success_message})








from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing_page.html')


def welcome_view(request):
    # No context needed for a static page
    return render(request, 'welcome.html')




















    import os
from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.conf import settings
from login.models import VisitorCount



def welcome(request):
    # Fetch the visitor count object or create one if it doesn't exist
    visitor_count, created = VisitorCount.objects.get_or_create(id=1)
    visitor_count.count += 1  # Increment the visitor count
    visitor_count.save()  # Save the updated count
    
    # Pass the count to the template
    context = {'visitor_count': visitor_count.count}
    return render(request, 'welcome.html', context)
from django.contrib.auth.decorators import login_required

@login_required
def subject_page(request):
    # Path to the 'subjects' directory where your folders are located
    subjects_folder_path = '/Users/vipul/Desktop/oo/pyq/subjects'

    # Get the folder names (directories only)
    subjects = [
        name for name in os.listdir(subjects_folder_path)
        if os.path.isdir(os.path.join(subjects_folder_path, name))
    ]

    return render(request, 'subjects.html', {'subjects': subjects})

def subject_details(request, subject):
    # Path to the main 'subjects' directory
    subjects_folder_path = '/Users/vipul/Desktop/oo/pyq/subjects'

    # Full path to the selected subject directory
    subject_path = os.path.join(subjects_folder_path, subject)

    # Check if the subject folder exists
    if not os.path.isdir(subject_path):
        raise Http404(f"Subject '{subject}' not found.")

    # List files and folders in the subject directory
    files_and_folders = os.listdir(subject_path)
    
    # Separate files and folders
    folders = [item for item in files_and_folders if os.path.isdir(os.path.join(subject_path, item))]
    files = [item for item in files_and_folders if os.path.isfile(os.path.join(subject_path, item))]

    # Context for rendering the template
    context = {
        'subject': subject,
        'folders': folders,  # List of folders
        'files': files       # List of files (optional, if needed elsewhere)
    }

    return render(request, 'subject_details.html', context)





from django.shortcuts import render, get_object_or_404
from django.http import Http404
import os

from django.shortcuts import render, get_object_or_404
import os
from django.http import Http404

import os
from django.shortcuts import render
from django.http import Http404
from django.conf import settings

import os
from django.shortcuts import render
from django.http import Http404
from django.conf import settings

def folder_details(request, subject, folder):
    # Path to the subject's folder
    subjects_folder_path = '/Users/vipul/Desktop/oo/pyq/subjects'
    subject_path = os.path.join(subjects_folder_path, subject)

    # Check if the subject folder exists
    if not os.path.isdir(subject_path):
        raise Http404(f"Subject '{subject}' not found.")

    # Full path to the selected folder
    folder_path = os.path.join(subject_path, folder)

    # Check if the folder exists
    if not os.path.isdir(folder_path):
        raise Http404(f"Folder '{folder}' not found in subject '{subject}'.")

    # List files in the selected folder
    files = os.listdir(folder_path)

    # Construct URLs for the files
    file_urls = [
        {
            'name': file,
            'url': os.path.join(settings.MEDIA_URL, subject, folder, file)  # Assuming MEDIA_URL is configured
        }
        for file in files if os.path.isfile(os.path.join(folder_path, file))
    ]

    # Context for rendering the template
    context = {
        'subject': subject,
        'folder': folder,
        'files': file_urls  # List of files with URLs
    }

    return render(request, 'folder_details.html', context)



from django.http import JsonResponse
from django.shortcuts import render
from .models import VisitorCount

def welcome_view(request):
    # Get or create visitor count
    visitor_count, created = VisitorCount.objects.get_or_create(id=1)
    return render(request, 'welcome.html', {'visitor_count': visitor_count.count})


def visitor_count_view(request):
    count = VisitorCount.increment()
    return JsonResponse({"count": count})





