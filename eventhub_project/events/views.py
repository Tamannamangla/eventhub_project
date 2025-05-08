from django.shortcuts import render,redirect ,get_object_or_404 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AdminProfile,EventManager , Feedback , Event
from .forms import AdminFullForm, EventForm
import requests

User = get_user_model() 

FLASK_API_BASE = "http://127.0.0.1:8080"

def all_events(request):
    try:
        headers = {"Accept": "application/json"}
        response = requests.get(f"{FLASK_API_BASE}/api/events",headers=headers)
        response.raise_for_status()

        print(" Raw Response JSON:", response.json()) 
        event_dicts = response.json().get("events", [])
        print(" Extracted events:", event_dicts)
        
        # Convert list of dicts to list of namedtuples for dot-access in templates
        Event = namedtuple("Event", event_dicts[0].keys()) if event_dicts else None
        events = [Event(**{**e, "id": int(e["id"])}) for e in event_dicts] if Event else []

        
    except requests.exceptions.RequestException:
        events = []

    return render(request, 'event_list.html', {"events": events})

def all_feedbacks(request):
    try:
        response = requests.get(f"{FLASK_API_BASE}/api/feedback")
        response.raise_for_status()
        feedbacks = response.json().get("feedbacks", [])
    except requests.exceptions.RequestException:
        feedbacks = []
    return render(request, 'feedback_list.html', {"feedbacks": feedbacks})


def all_users(request):
    try:
        response = requests.get(f"{FLASK_API_BASE}/api/users")
        response.raise_for_status()
        users = response.json().get("users", [])
    except requests.exceptions.RequestException:
        users = []
        
    return render(request, 'user_list.html', {"users": users})

def edit__event(request, event_id):
    event_url = f"{FLASK_API_BASE}/api/events/{event_id}"

    if request.method == "POST":
        updated_data = {
            "name": request.POST.get("name"),
            "description": request.POST.get("description"),
            "date": request.POST.get("date"),
            "location": request.POST.get("location"),
            "category": request.POST.get("category"),
        }

        try:
            response = requests.put(event_url, json=updated_data)
            response.raise_for_status()
            messages.success(request, "Event updated successfully.")
            return redirect('all_events')
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error updating event: {e}")

    try:
        response = requests.get(event_url)
        response.raise_for_status()
        event_data = response.json() 
        Event = namedtuple("Event", event_data.keys())
        event = Event(**event_data) 
    except requests.exceptions.RequestException:
        event = None
        messages.error(request, "Failed to load event.")

    return render(request, "edit__event.html", {"event": event})

def delete__event(request, event_id):
    if request.method == "POST":
        # Ensure the event_id is a valid positive integer
        if not isinstance(event_id, int) or event_id <= 0:
            messages.error(request, "Invalid Event ID.")
            return redirect('all_events')

        try:
            response = requests.delete(f"{FLASK_API_BASE}/api/events/{event_id}")
            response.raise_for_status()

            if response.status_code == 204:
                messages.success(request, "Event deleted successfully.")
            else:
                messages.warning(request, "Unexpected response from the server.")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                messages.error(request, "Event not found.")
            else:
                messages.error(request, f"HTTP Error: {e}")

        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error deleting event: {e}")

    return redirect('all_events')
   
# Create your views here.
def about(request):
    return render(request, 'events/aboutus.html')

@login_required
def contact(request):
    return render(request, 'events/contact.html')

def privacy(request):
    return render(request, 'privacypolicy.html')

@login_required
def home(request):
    return render(request,'home.html')

def event(request):
    event = Event.objects.all()
    return render(request, 'event.html', {'event': event})

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password != cpassword:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
        else:
            try:
                validate_password(password)
                User.objects.create_user(
                    email=email,
                    name=name,
                    phone=phone,
                    gender=gender,
                    dob=dob,
                    address=address,
                    password=password
                )
                messages.success(request, 'Registration successful! You can now login.')
                return redirect('login')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        selected_role = request.POST.get('role')
        user = authenticate(request, email=email, password=password)
        if user:
        # Determine if the role matches the actual user status
            if user.role == selected_role:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('home') 
            else:
                messages.error(request, "Invalid credentials: Role mismatch")
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    next_url = request.GET.get('next', 'index')  # fallback = 'index'
    return redirect(next_url)

def index(request):
    return render(request,'index.html')
from collections import namedtuple
@login_required
def super_admin_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "Login required")
        return redirect('login')

    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access")
        return redirect('home') 

    return render(request, 'super_admin_dashboard.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "Login required")
        return redirect('login')

    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "Unauthorized access")
        return redirect('home')

    return render(request, 'admin_dashboard.html')

@login_required
def event_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "Login required")
        return redirect('login')

    if request.user.role != 'event_manager' and not request.user.is_superuser:
        messages.error(request, "Unauthorized access")
        return redirect('events:home')
    events = Event.objects.all()
    return render(request, 'dashboard.html', {'events': events})

def add_admin(request):
    if request.method == 'POST':
        form = AdminFullForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                gender=form.cleaned_data['gender'],
                dob=form.cleaned_data['dob'],
                address=form.cleaned_data['address'],
                password=form.cleaned_data['password'],
                role='admin',
                is_staff=True
            )

            # Step 2: Create AdminProfile linked to user
            admin_profile = form.save(commit=False)
            admin_profile.user = user
            admin_profile.save()

            return redirect('list_admins')  # or wherever
    else:
        form = AdminFullForm()

    return render(request, 'add_admin.html', {'form': form})


def list_admins(request):
    admins = AdminProfile.objects.all()
    return render(request, 'list_admins.html', {'admins': admins})

def edit_admin(request, admin_id):
    admin = get_object_or_404(AdminProfile, id=admin_id)
    user = admin.user  # linked CustomUser

    if request.method == 'POST':
        form = AdminFullForm(request.POST, instance=admin)
        form.fields.pop('password', None) 
        if form.is_valid():
            admin_profile = form.save(commit=False)
            user.name = form.cleaned_data['name']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            user.gender = form.cleaned_data['gender']
            user.dob = form.cleaned_data['dob']
            user.address = form.cleaned_data['address']
            user.save()

            admin_profile.save()
            return redirect('list_admins')
    else:
        form = AdminFullForm(initial={
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'gender': user.gender,
            'dob': user.dob,
            'address': user.address,
            'hobbies': admin.hobbies,
            'bio': admin.bio,
            'social_media': admin.social_media,
            'notifications': admin.notifications,
        }, instance=admin)
        form.fields.pop('password', None) 

    return render(request, 'edit_admin.html', {'form': form})

def delete_admin(request, admin_id):
    admin = get_object_or_404(AdminProfile, id=admin_id)
    user = admin.user
    admin.delete()
    user.delete()  
    return redirect('list_admins')

# event managers
@login_required
def add_event_manager(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        hobbies = request.POST.get('hobbies')
        address = request.POST.get('address')
        if password:
            EventManager.password=password

        if EventManager.objects.filter(email=email).exists():
            messages.error(request, 'An event manager with this email already exists.')
            return redirect('add_event_manager')

        if EventManager.objects.filter(user=request.user, name=name).exists():
            messages.error(request, 'User with this name already exists.')
        else:
            EventManager.objects.create(
                user=request.user,
                name=name,
                email=email,
                phone=phone,
                password=password,
                gender=gender,
                hobbies=hobbies,
                address=address
            )
            messages.success(request, 'Manager added successfully!')
            return redirect('add_event_manager')

    if request.user.is_superuser:
        event_manager = EventManager.objects.all()
    else:
        event_manager = EventManager.objects.filter(user=request.user)
    return render(request, 'add_event_manager.html', context={'event_manager': event_manager})



@login_required
def delete_event_manager(request, product_id):
    product = EventManager.objects.get(id=product_id)
    if request.user == product.user or request.user.is_superuser:
        product.delete()
        messages.success(request, 'Manager deleted successfully!')
    else:
        messages.error(
            request, 'You are not authorized to delete this product.')
    return redirect('add_event_manager')

@login_required
def update_event_manager(request, product_id):
    event_manager = EventManager.objects.get(id=product_id)


    # Authorization: Only the product owner or a superuser can update
    if request.user != event_manager.user and not request.user.is_superuser:
        messages.error(
            request, "You are not authorized to update this event_manager.")
        return redirect('add_event_manager')


    if request.method == 'POST':
        event_manager.name = request.POST.get('name')
        event_manager.phone = request.POST.get('phone')
        event_manager.password = request.POST.get('password')  # 👈 Ensure this is included
        event_manager.gender = request.POST.get('gender')
        event_manager.hobbies = request.POST.get('hobbies')
        event_manager.address = request.POST.get('address')
        

        # Ensure unique event_manager name per user
        if EventManager.objects.filter(user=event_manager.user, name=event_manager.name).exclude(id=event_manager.id).exists():
            messages.error(request, "Manager with this name already exists.")
        else:
            event_manager.save()
            messages.success(request, "Manager updated successfully!")
            return redirect('add_event_manager')


    return render(request, 'update_event_manager.html', {'event_manager': event_manager})

@login_required
def add_event(request):
    form = EventForm(request.POST or  None) 
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'form.html', {'form': form, 'title': 'Add Event'})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'form.html', {'form': form, 'title': 'Edit Event'})


def view_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.view()
        return redirect('dashboard')
    return render(request, 'delete_confirm.html', {'event': event})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event.delete()
        return redirect('dashboard') 
    return render(request, 'delete.html', {'event': event})

# profile view
@login_required
def profile(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied: You are not authorized to view this page.")
        return redirect('super_admin_dashboard')
    
    # Fetch the related AdminProfile (or whatever model you're using)
    try:
        user_profile = AdminProfile.objects.get(user=request.user)
    except AdminProfile.DoesNotExist:
        user_profile = None

    return render(request, 'profile.html', {
        'user_profile': user_profile,
        'profile': request.user
    })


@login_required
def edit_profile(request):
    try:
        user_profile = AdminProfile.objects.get(user=request.user)
    except AdminProfile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        form = AdminFullForm(request.POST, instance=user_profile)
        form.fields.pop('password', None)  # no password edit here
        form.fields.pop('role', None)

        if form.is_valid():
            
            profile = form.save(commit=False)
            user = request.user
            user.name = form.cleaned_data['name']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            user.gender = form.cleaned_data['gender']
            user.dob = form.cleaned_data['dob']
            user.address = form.cleaned_data['address']
            user.role = request.user.role if request.user.role else 'user'

            print("ROLE BEFORE SAVE:", user.role)
            user.save()
            profile.user = user
            profile.save()

            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
            pass
        else:
            print("Form Errors:", form.errors)  # <-- Yeh daal
    else:
        form = AdminFullForm(initial={
            'name': request.user.name,
            'email': request.user.email,
            'phone': request.user.phone,
            'gender': request.user.gender,
            'dob': request.user.dob,
            'address': request.user.address,
            'hobbies': user_profile.hobbies if user_profile else '',
            'bio': user_profile.bio if user_profile else '',
            'social_media': user_profile.social_media if user_profile else '',
            'notifications': user_profile.notifications if user_profile else False,
        }, instance=user_profile)
        form.fields.pop('password', None)
        form.fields.pop('role', None) 

    return render(request, 'edit_profile.html', {'form': form})


def feedback_view(request):
    if request.method == 'POST':
        feedback_type = request.POST.get('feedback')
        name = request.POST.get('name')
        email = request.POST.get('email')
        description = request.POST.get('description')

        if feedback_type and name and email and description:
            Feedback.objects.create(
                feedback_type=feedback_type,
                name=name,
                email=email,
                description=description
            )
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback')
        else:
            messages.error(request, 'Please fill out all fields.')

    return render(request, 'feedback.html')


def gallery(request):
    return render(request,'gallery.html')

def birthday1(request):
    return render(request,'birthday/birthday1.html')

def birthday2(request):
    return render(request,'birthday/birthday1.html')

def birthday3(request):
    return render(request,'birthday/birthday1.html')

def party1(request):
    return render(request,'retirementparty/party1.html')

def party2(request):
    return render(request,'retirementparty/party2.html')

def wed1(request):
    return render(request,'weedings/wed1.html')