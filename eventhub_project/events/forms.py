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
        exclude = ['user']  # We handle user manually in the view

# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = ['name', 'category', 'location', 'date', 'description']
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control rounded-3 shadow-sm',
#                 'placeholder': 'Enter event name'
#             }),
#             'category': forms.Select(attrs={
#                 'class': 'form-select rounded-3 shadow-sm'
#             }),
#             'location': forms.TextInput(attrs={
#                 'class': 'form-control rounded-3 shadow-sm',
#                 'placeholder': 'Enter location'
#             }),
#             'date': forms.DateInput(attrs={
#                 'class': 'form-control rounded-3 shadow-sm',
#                 'type': 'date'
#             }),
#             'description': forms.Textarea(attrs={
#                 'class': 'form-control rounded-3 shadow-sm',
#                 'rows': 4,
#                 'placeholder': 'Write something about the event...'
#             }),
#             'image': forms.ClearableFileInput(attrs={
#                 'class': 'form-control rounded-3 shadow-sm',
#                 'accept': 'image/*'
#             }),
#         }
from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Enter event name',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control mb-3',
                'type': 'date'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Enter location',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'rows': 4,
                'placeholder': 'Event description...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'accept': 'image/*'
      }),

        }
        
        
        def __init__(self, *args, **kwargs):
            super(EventForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.label_suffix = ''
                existing_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{existing_class} shadow-sm rounded border border-secondary'
                field.widget.attrs['style'] = 'padding: 10px;'