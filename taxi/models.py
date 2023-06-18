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


def validator_license_number(value):
    if len(value) != 8:
        raise ValidationError("Consist only of 8 characters")
    if not (value[:3].isupper() and value[:3].isalpha()):
        raise ValidationError(
            "First 3 characters must be uppercase letters"
        )
    if not value[3:].isdigit():
        raise ValidationError(
            "Last 5 characters must be digits"
        )


class Driver(AbstractUser):
    license_number = models.CharField(max_length=255,
                                      unique=True,
                                      validators=[validator_license_number]
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
