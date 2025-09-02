from django.contrib import admin

# Register your models here.
from .models import Car, Service, Order, OrderLine, OrderReview


class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0
    fields = ['service', 'quantity', 'line_sum']
    readonly_fields = ['line_sum']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date', 'total', 'status', 'car_return', 'user']
    inlines = [OrderLineInLine]
    readonly_fields = ['date', 'total']
    list_editable = ['status', 'user', 'car_return']

    fieldsets = [
        ("General", {"fields": ['car', 'date', 'total', 'status', 'car_return', 'user', 'description']})
    ]


class CarAdmin(admin.ModelAdmin):
    list_display = ["make", "model", "client_name", "license_plate", "vin_code"]
    list_filter = ["client_name", "make", "model"]
    search_fields = ["license_plate", "vin_code"]

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'price']
    list_editable = ['name', 'price']

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'service', 'service__price', 'quantity', 'line_sum']





admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(OrderReview)
