from django.db import models

from django.conf import settings

class Ticket(models.Model):
    CATEGORY_CHOICES = [
        ('Music', 'Music'),
        ('Art', 'Art'),
        ('Food', 'Food'),
        ('Business', 'Business'),
        ('Hobbies', 'Hobbies'),
        ('Nightlife', 'Nightlife'),
        ('Holidays', 'Holidays'),
        ('Dates', 'Dates'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) 
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    time = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    image = models.ImageField(upload_to='ticket_images/')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)  # Assuming a user can book multiple tickets
    image = models.ImageField(upload_to='booking_images/', null=True, blank=True)  # Optional image field

    def __str__(self):
        return f"{self.user.email} booked {self.ticket.name} (Quantity: {self.quantity}) on {self.booking_date}"








