from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,authenticate
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .models import *

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    return render(request, 'home.html', {})

from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect user based on is_service_provider flag
                if user.is_service_provider:
                    return redirect(reverse('service_provider_dashboard'))
                else:
                    return redirect(reverse('user_dashboard'))
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def user_dashboard(request):
    # Your logic for the user dashboard
    return render(request, 'dashboard_user.html', {})

def service_provider_dashboard(request):
    bookings= Booking.objects.all()
    for booking in bookings:
        if booking.confirmed == False:
            display = True
        else:
            display = False    
    return render(request, 'dashboard_service_provider.html', {"bookings":bookings,'display':display})


def search_services(request):
    query = request.GET.get('query', '')
    print(query)
    services = Service.objects.filter(name=query) if query else Service.objects.all()
    print(services)
    return render(request, 'dashboard_user.html', {'services': services})

def book_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.save()
            return redirect('user_dashboard')  # Redirect to a booking success page
    else:
        form = BookingForm()
    return render(request, 'book_service.html', {'form': form, 'service': service})

def view_bookings(request):
    if request.user.is_service_provider:
        bookings = Booking.objects.filter(service__provider=request.user).order_by('-date_time')
        return render(request, 'provider_dashboard.html', {'bookings': bookings})
    else:
        return redirect('home')  # or some other appropriate redirect

def update_booking_status(request, booking_id, status):
    if request.user.is_service_provider:
        booking = get_object_or_404(Booking, id=booking_id)
        if status == 'accept':
            booking.status = True
        else:
            booking.status = False 
        booking.confirmed=True    
        booking.save()
        return redirect('service_provider_dashboard')
    else:
        return redirect('home')
    
def service_provider_profile(request):
    if not request.user.is_authenticated or not request.user.is_service_provider:
        return redirect('home')  # Redirect to home if not authorized or not a provider

    # Get all accepted bookings for the logged-in service provider
    services = Service.objects.filter(service_provider_id=request.user)
    accepted_bookings = []
    for service in services: 
        accepted_bookings.append(Booking.objects.filter(service_id=service,status=True))
    # Optional: Add profile information if stored separately
    profile = User.objects.filter(username=request.user)[0]
    print(accepted_bookings[0][0].user)
    context = {
        'profile': profile,
        'bookings': accepted_bookings[0]
    }
    return render(request, 'provider_profile.html', context)




from .forms import ServiceForm
from django.http import JsonResponse

def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            new_service = form.save(commit=False)
            new_service.service_provider = request.user  # Set the provider to the logged-in user
            new_service.save()
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False}, status=400)
    else:
        form = ServiceForm()
    return render(request, 'add_service.html', {'form': form})
