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


def driver_license_number_validate(value):
    error = ""
    if len(value) != 8:
        error += "Driver license number should consist only of 8 characters"
    if not value[0:3].isalpha() or not value[0:3].isupper():
        error += "; \n" if error else ""
        error += "First 3 characters of driver license number " \
                 "should be uppercase letters"
    if not value[-5:].isdigit():
        error += "; \n" if error else ""
        error += "Last 5 characters of driver license number " \
                 "should be are digits"

    if error:
        raise ValidationError(error, params={"value": value},)


class Driver(AbstractUser):
    license_number = models.CharField(
        max_length=255,
        unique=True,
        validators=[driver_license_number_validate]
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

    def get_absolute_url(self):
        return reverse("taxi:car-detail", kwargs={"pk": self.pk})
