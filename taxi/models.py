from django.core.validators import RegexValidator, MinLengthValidator
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


class Driver(AbstractUser):
    uppercase_validator = RegexValidator(
        regex=r"^[A-Z]{3}",
        message="First 3 letters must be uppercase."
    )
    length_validator = RegexValidator(
        r"^.{8}$", message="License number must be 8 characters long."
    )
    digits_validator = RegexValidator(
        regex=r"\d{5}$",
        message="Last 5 characters must be digits."
    )
    license_number = models.CharField(
        max_length=255,
        unique=True,
        validators=[uppercase_validator, length_validator, digits_validator]
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
