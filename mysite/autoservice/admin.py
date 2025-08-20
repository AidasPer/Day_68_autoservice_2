from django.contrib import admin

# Register your models here.
from .models import Car, Service, Order, OrderLine


class OrderAdmin(admin.ModelAdmin):
    list_display = ["car", "date"]


class CarAdmin(admin.ModelAdmin):
    list_display = ["make", "model", "client_name", "license_plate", "vin_code"]
    list_filter = ["client_name", "make", "model"]
    search_fields = ["license_plate", "vin_code"]

class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]




class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0




admin.site.register(Car, CarAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)