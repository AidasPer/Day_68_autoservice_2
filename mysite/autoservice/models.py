from django.db import models
from django.contrib.auth.models import User, AbstractUser, UserManager
from django.utils import timezone
from tinymce.models import HTMLField
# Create your models here.


class CustomUser(AbstractUser):
    photo = models.ImageField(verbose_name="Photo", upload_to="profile_pics" , null=True, blank=True)
    location = models.TextField(verbose_name="Location", null=True, blank=True)

    objects = UserManager()


class Car(models.Model):
    make = models.CharField(verbose_name="Make", max_length=14)
    model = models.CharField(verbose_name="Model", max_length=14)
    license_plate = models.CharField(verbose_name="License plate", max_length=14)
    vin_code = models.CharField(verbose_name="Vin code", max_length=14)
    client_name = models.CharField(verbose_name="Client name", max_length=14)
    car_image = models.ImageField('Car image', upload_to='car_images', null=True, blank=True)

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
    user = models.ForeignKey(to="autoservice.CustomUser", verbose_name="User", on_delete=models.SET_NULL, null=True, blank=True)
    car_return = models.DateField(verbose_name="Return date", null=True, blank=True)
    description = HTMLField(verbose_name="Description", max_length=2000, null=True, blank=True)

    ORDER_STATUS = (
        ('c', 'Created'),
        ('p', 'In Progress'),
        ('f', 'Finished'),
        ('x', 'Cancelled'),
    )

    status = models.CharField(verbose_name="Status", choices=ORDER_STATUS, max_length=1, blank=True, default='c')

    def is_returned(self):
        return self.car_return and self.car_return < timezone.now().date()

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


    class Meta:
        verbose_name = "Order line"
        verbose_name_plural = "Order lines"

class OrderReview(models.Model):
    order = models.ForeignKey(to="order",verbose_name="order", on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(to="autoservice.CustomUser",verbose_name="Author", on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(verbose_name="Content")
    date_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)


    def __str__(self):
        return f"{self.author} - {self.order}({self.date_created})"

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Order comment"
        verbose_name_plural = "Order comments"