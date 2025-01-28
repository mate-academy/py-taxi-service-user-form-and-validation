from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse, reverse_lazy
from django.views import generic


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


class Driver(AbstractUser):
    license_number = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "driver"
        verbose_name_plural = "drivers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.pk})


class DriverCreateView(generic.CreateView):
    form_class = Driver
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_forms.html"


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    template_name = "taxi/driver_format_confirm_delete.html"
    success_url = reverse_lazy("taxi:driver-delete")


class Car(models.Model):
    model = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    drivers = models.ManyToManyField(Driver, related_name="cars")

    def __str__(self):
        return self.model
