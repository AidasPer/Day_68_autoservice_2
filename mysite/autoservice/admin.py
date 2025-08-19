from django.contrib import admin

# Register your models here.
from .models import Car, Service, Order

admin.site.register(Car)
admin.site.register(Service)
admin.site.register(Order)