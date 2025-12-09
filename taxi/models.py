import re

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


def validate_license(license_number):
    """
    Validate that license consists of 3 uppercase letters and 5 digits.
    Raises multiple validation errors with specific details.
    """
    errors = []

    if len(license_number) != 8:
        errors.append("License must be exactly 8 characters long.")

    if not re.match(r"^[A-Z]{3}", license_number):
        errors.append("The first 3 characters must be uppercase letters.")

    if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
        errors.append("The last 5 characters must be digits.")

    if errors:
        raise ValidationError(errors)


class Driver(AbstractUser):
    license_number = models.CharField(
        max_length=8,
        unique=True,
        validators=[validate_license]
    )

    class Meta:
        verbose_name = "driver"
        verbose_name_plural = "drivers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.pk})


class Car(models.Model):
    model = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    drivers = models.ManyToManyField(Driver, related_name="cars")

    def __str__(self):
        return self.model
