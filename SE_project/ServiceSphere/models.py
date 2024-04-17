from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_service_provider = models.BooleanField(default=False)
 
class Service(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    category = models.CharField(max_length=100,null=True)
    available = models.BooleanField(default=True,null=True)
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} - {self.service.name} on {self.date_time}"


