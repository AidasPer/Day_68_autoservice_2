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

class Service(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    price = models.FloatField(verbose_name="Price")

    def __str__(self):
        return self.name


class Order(models.Model):
    date = models.DateField(verbose_name="Date", null=True, blank=True)
    car = models.ForeignKey(to="Car", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order {self.date}: {self.car}"

