from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import forms
from django.urls import reverse


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

    def clean_license_number(self):
        if len(self.license_number) != 8:
            raise forms.ValidationError(
                "The license must be 8 characters long"
            )
        if (not self.license_number[:3].isupper()
                or not self.license_number[:3].isalpha()):
            raise forms.ValidationError(
                "The first 3 characters must be uppercase letters"
            )
        if not self.license_number[-5:].isdigit():
            raise forms.ValidationError(
                "The last 5 characters must be digits"
            )


class Car(models.Model):
    model = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    drivers = models.ManyToManyField(Driver, related_name="cars")

    def __str__(self):
        return self.model
