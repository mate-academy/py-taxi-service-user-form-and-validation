from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


def validate_license_number(value):
    if len(value) != 8:
        raise ValidationError("License must be exactly 8 characters")

    first_letters = value[:3]
    last_digits = value[3:]

    if not first_letters.isalpha() or not first_letters.isupper():
        raise ValidationError("First 3 characters must be uppercase letters")

    if not last_digits.isdigit():
        raise ValidationError("Last 5 characters must be digits")

    return value


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


class Driver(AbstractUser):
    license_number = models.CharField(
        max_length=255, unique=True, validators=[validate_license_number]
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
