from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


def license_number_validator(license_number):
    has_digit = any(char.isdigit() for char in license_number[:3])
    if (
        has_digit
        or not license_number[:3].upper().isupper()
        or not license_number[3:].isdigit()
        or len(license_number) != 8
    ):
        raise ValidationError(
            "The code must consist of 8 characters"
            " with the first 3 uppercase letters and the last 5 digits."
        )

    return license_number


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


class Driver(AbstractUser):
    license_number = models.CharField(
        max_length=8, unique=True, validators=[license_number_validator]
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
