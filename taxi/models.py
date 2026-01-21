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


def clean_license_number_field(value):
    if len(value) != 8:
        raise ValidationError(
            "Length of License number should "
            "be consist only of 8 characters"
        )
    elif not (
            value[0:3].isalpha()
            and value[0:3].isupper()
    ):
        raise ValidationError(
            "First 3 characters should be uppercase letters"
        )
    elif not value[3:].isdigit():
        raise ValidationError(
            "Last 5 characters should be are digits"
        )


class Driver(AbstractUser):
    license_number = models.CharField(
        max_length=255,
        unique=True,
        validators=[clean_license_number_field],
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
