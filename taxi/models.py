from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
import re
from django.core.exceptions import ValidationError


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


def validate_license_number(value):
    if not re.fullmatch(r"[A-Z]{3}\d{5}", value):
        raise ValidationError(
            "License number must have 3 uppercase "
            "letters followed by 5 digits (e.g., ABC12345)."
        )


class Driver(AbstractUser):
    license_number = models.CharField(
        max_length=8, unique=True, validators=[validate_license_number]
    )


class Car(models.Model):
    model = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    drivers = models.ManyToManyField(Driver, related_name="cars")

    def __str__(self):
        return self.model
