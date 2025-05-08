from django.urls import path
from . import views

urlpatterns = [
    path('music',views.music,name='music'),
    path('art/', views.art, name='art'),
    path('food/', views.food, name='food'),
    path('hobbies/', views.hobbies, name='hobbies'),
    path('business/', views.business, name='business'),
    path('nightlife/', views.nightlife, name='nightlife'),
    path('holidays/', views.holiday, name='holidays'),
    path('dates/', views.dates, name='dates'),
    path('index2', views.index2, name='index2'),
    path('dashboard3', views.dashboard3, name='dashboard3'),

    path('ticket/edit/<int:ticket_id>/', views.edit_ticket, name='edit_ticket'),
    path('ticket/delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),

    path('buy_ticket/<int:ticket_id>/', views.buy_ticket, name='buy_ticket'),
    path('cart/', views.view_cart, name='view_cart'),
    path('payment/', views.payment_view, name='payment'),

    path('api/tickets/', views.TicketListCreateAPIView.as_view(), name='ticket-list-create'),
    path('api/bookings/', views.BookingListCreateAPIView.as_view(), name='booking-list-create'),
]

app_name = 'bookings'
