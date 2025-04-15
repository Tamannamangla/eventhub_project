from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, phone, gender, dob, address, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            phone=phone,
            gender=gender,
            dob=dob,
            address=address,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, phone, gender, dob, address, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not password:
            raise ValueError("Superusers must have a password.")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, name, phone, gender, dob, address, password, **extra_fields)

class CustomUser(AbstractUser):
    
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('event_manager', 'Event Manager'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True)

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    
    username = None  # Remove default username field

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'address', 'gender', 'dob']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class AdminProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('event_manager', 'Event Manager')
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  # use an existing user ID
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    hobbies = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    address = models.TextField(blank=True)
    social_media = models.TextField(blank=True)
    notifications = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

class EventManager(models.Model):
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('other', 'Other'),
    ]

    # One-to-many relationship with User
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    password = models.CharField(max_length=128)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    hobbies = models.TextField(default='None')
    address = models.TextField(default='Unknown')


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('user', 'name')
        
class Feedback(models.Model):
    FEEDBACK_CHOICES = [
        ('comments', 'Comments'),
        ('bug_report', 'Bug Report'),
        ('questions', 'Questions'),
    ]

    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_CHOICES)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.feedback_type}"
    

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    # category = models.CharField(max_length=50)
    CATEGORY_CHOICES = [
        ('ceremony', 'Ceremony'),
        ('birthday', 'Birthday'),
        ('anniversary', 'Anniversary'),
        ('wedding', 'Wedding'),
        ('baby-shower', 'Baby Shower'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name



