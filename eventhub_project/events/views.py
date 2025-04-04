from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, 'events/aboutus.html')
def contact(request):
    return render(request, 'events/contact.html')
