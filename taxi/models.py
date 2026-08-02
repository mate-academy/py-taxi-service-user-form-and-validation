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


class Driver(AbstractUser):
    LICENSE_LENGTH = 8
    license_number = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "driver"
        verbose_name_plural = "drivers"

    def clean(self) -> None:
        super().clean()

        license_number = self.license_number

        if len(license_number) != self.LICENSE_LENGTH:
            raise ValidationError({
                "license_number": "License must contain exactly 8 characters."
            })

        first_part = license_number[:3]
        last_part = license_number[3:]

        if not first_part.isalpha() or not first_part.isupper():
            raise ValidationError({
                "license_number":
                    "The first three characters must be uppercase letters."
            })

        if not last_part.isdigit():
            raise ValidationError({
                "license_number": "The last five characters must be digits."
            })

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
