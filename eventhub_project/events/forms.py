from django import forms
from .models import AdminProfile,Event
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminFullForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(max_length=15)
    gender = forms.ChoiceField(choices=AdminProfile.GENDER_CHOICES)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = AdminProfile
        exclude = ['user'] 

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'