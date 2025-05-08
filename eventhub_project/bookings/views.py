
from django.shortcuts import render,redirect ,get_object_or_404 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import TicketForm
from .models import Ticket, Booking
from rest_framework import generics, permissions
from .models import Ticket, Booking
from .serializers import TicketSerializer, BookingSerializer
from collections import defaultdict

# Create your views here.

def index2(request):
    return render(request, 'index2.html')

@login_required
def dashboard3(request):
    form = TicketForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        ticket = form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        return redirect('bookings:dashboard3')

    tickets = Ticket.objects.all().order_by('-id')

    categorized_tickets = defaultdict(list)
    for ticket in tickets:
        categorized_tickets[ticket.category].append(ticket)

    return render(request, 'dashboard3.html', {
        'form': form,
        'categorized_tickets': dict(categorized_tickets),
    })

def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('bookings:dashboard3')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'edit_ticket.html', {'form': form})

def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.delete()
    return redirect('bookings:dashboard3')
    
def music(request):
    tickets = Ticket.objects.filter(category='Music')
    return render(request, 'music.html', {'tickets': tickets})

def art(request):
    tickets = Ticket.objects.filter(category='Art')
    return render(request, 'art.html', {'tickets': tickets})

def food(request):
    tickets = Ticket.objects.filter(category='Food')
    return render(request, 'food.html', {'tickets': tickets})

def business(request):
    tickets = Ticket.objects.filter(category='Business')
    return render(request, 'business.html', {'tickets': tickets})

def hobbies(request):
    tickets = Ticket.objects.filter(category='Hobbies')
    return render(request, 'hobbies.html', {'tickets': tickets})

def nightlife(request):
    tickets = Ticket.objects.filter(category='Nightlife')
    return render(request, 'nights.html', {'tickets': tickets})

def holiday(request):
    tickets = Ticket.objects.filter(category='Holidays')
    return render(request, 'holiday.html', {'tickets': tickets})

def dates(request):
    tickets = Ticket.objects.filter(category='Dates')
    return render(request, 'dates.html', {'tickets': tickets})


@login_required
def buy_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

   
    booking = Booking.objects.filter(user=request.user, ticket=ticket).first()

    if request.method == 'POST':
        if booking:
        
            booking.quantity += 1
            booking.save()
        else:
        
            booking = Booking.objects.create(
                user=request.user,
                ticket=ticket,
                quantity=1
            )

        return redirect('bookings:view_cart')  

    return render(request, 'cart.html', {'ticket': ticket})

from django.urls import reverse

@login_required
def view_cart(request):
    bookings = Booking.objects.filter(user=request.user)
    total = sum(float(b.ticket.price) * b.quantity for b in bookings)

    # If updating quantity
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')

        booking = get_object_or_404(Booking, id=booking_id, user=request.user)

        if action == 'increase':
            booking.quantity += 1
            booking.save()
        elif action == 'decrease' and booking.quantity > 1:
            booking.quantity -= 1
            booking.save()
        elif action == 'delete':
            booking.delete()

        return redirect('bookings:view_cart')

    return render(request, 'cart.html', {
        'bookings': bookings,
        'total': total,
        'address': request.user.address  # from your CustomUser
    })
@login_required
def payment_view(request):
    bookings = Booking.objects.filter(user=request.user)
    total = sum(float(b.ticket.price) * b.quantity for b in bookings)

    return render(request, 'payment.html', {
        'bookings': bookings,
        'total': total
    })

class TicketListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
