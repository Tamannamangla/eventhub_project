from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'image', 'location', 'time', 'price', 'category', 'total_tickets', 'available_quantity']

        