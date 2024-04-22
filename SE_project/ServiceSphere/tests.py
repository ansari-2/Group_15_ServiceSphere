from django.test import TestCase, Client
from django import setup
import os

from django.urls import reverse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SE_project.settings")
setup()

from .models import Booking, Service, User

class ServiceTestCase(TestCase):
    def test_queryset_exists(self):
        qs = Service.objects.all()
        self.assertTrue(qs.exists())

    
    def test_queryset_exists2(self):
        qs = Service.objects.all()
        self.assertTrue(qs.exists())

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test service provider
        self.service_provider = User.objects.create_user(username='serviceprovider', password='testpassword')
        self.service_provider.is_service_provider = True
        self.service_provider.save()

        # Create a test service
        self.service = Service.objects.create(name='Test Service', description='Test Description', price=10, service_provider=self.service_provider)

        # Create a test booking
        self.booking = Booking.objects.create(user=self.user, service=self.service, date_time='2024-04-21 12:00:00')

    def test_register_view(self):
        from .views import register
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_user_dashboard_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_service_provider_dashboard_view(self):
        self.client.force_login(self.service_provider)
        response = self.client.get(reverse('service_provider_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_search_services_view(self):
        response = self.client.get(reverse('search_services') + '?query=Test Service')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Service')

    def test_book_service_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('book_service', args=[self.service.id]))
        self.assertEqual(response.status_code, 200)

    def test_update_booking_status_view(self):
        self.client.force_login(self.service_provider)
        response = self.client.post(reverse('update_booking_status', args=[self.booking.id, 'accept']))
        self.assertEqual(response.status_code, 302)  # Redirects after updating status

    def test_add_service_view(self):
        self.client.force_login(self.service_provider)
        response = self.client.get(reverse('add_service'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.user.delete()
        self.service_provider.delete()