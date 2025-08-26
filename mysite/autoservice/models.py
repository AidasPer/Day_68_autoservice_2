from django.db import models

# Create your models here.

class Car(models.Model):
    make = models.CharField(verbose_name="Make", max_length=14)
    model = models.CharField(verbose_name="Model", max_length=14)
    license_plate = models.CharField(verbose_name="License plate", max_length=14)
    vin_code = models.CharField(verbose_name="Vin code", max_length=14)
    client_name = models.CharField(verbose_name="Client name", max_length=14)

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"


class Service(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    price = models.FloatField(verbose_name="Price")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date", null=True, blank=True)
    car = models.ForeignKey(to="Car", on_delete=models.SET_NULL, null=True, blank=True)

    ORDER_STATUS = (
        ('c', 'Created'),
        ('p', 'In Progress'),
        ('f', 'Finished'),
        ('x', 'Cancelled'),
    )

    status = models.CharField(verbose_name="Status", choices=ORDER_STATUS, max_length=1, blank=True, default='c')

    def total(self):
        total = 0
        for line in self.lines.all():
            total += line.service.price * line.quantity
        return total

    def __str__(self):
        return f"Order {self.date}: {self.car}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name='lines')
    service = models.ForeignKey(to="Service", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()

    def line_sum(self):
        return self.service.price * self.quantity

    def __str__(self):
        return f"{self.service} ({self.service.price}) - {self.quantity}"
        return f"{self.service} ({self.service.price}) - {self.quantity}"

    class Meta:
        verbose_name = "Order line"
        verbose_name_plural = "Order lines"
