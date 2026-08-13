from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


def validate_license_number(license_number: str) -> None:
    if not (
        len(license_number) == 8
        and license_number[:3].isupper()
        and license_number[:3].isalpha()
        and license_number[3:].isdigit()
    ):
        raise ValidationError(
            "The code must consist "
            "of 3 uppercase letters "
            "followed by 5 digits "
            "(e.g., ABC12345)."
        )


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


class Driver(AbstractUser):
    license_number = models.CharField(
        max_length=8, validators=[validate_license_number]
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
