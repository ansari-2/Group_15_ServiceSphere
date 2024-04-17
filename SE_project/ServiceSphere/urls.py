from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
     path('login/', user_login, name='login'),
     path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
     path('home/', home, name='home'),
    path('dashboard/user/', user_dashboard, name='user_dashboard'),
     path('book/<int:service_id>/', book_service, name='book_service'),
    path('dashboard/service-provider/',service_provider_dashboard, name='service_provider_dashboard'),
    path('search_services/', search_services, name='search_services'),
    path('bookings/update/<int:booking_id>/<str:status>/', update_booking_status, name='update_booking_status'),
     path('provider/profile/', service_provider_profile, name='provider_profile'),
      path('add-service/', add_service, name='add_service'),

     

]
