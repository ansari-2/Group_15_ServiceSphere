from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Booking)
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')