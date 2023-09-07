from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


def validate_license_number(value):
    conditions = {
        "License should consist 8 characters":
            len(value) == 8,
        "First 3 characters should be uppercase letters":
            value[:3].isalpha() and value[:3].isupper(),
        "Last 5 characters should be digits":
            value[-5:].isdigit()
    }
    for message, value in conditions.items():
        if not value:
            raise ValidationError(f"{message}")


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


class Driver(AbstractUser):
    license_number = models.CharField(
        validators=[validate_license_number],
        max_length=255,
        unique=True
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
