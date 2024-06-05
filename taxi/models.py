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
    license_number = models.CharField(
        max_length=255,
        unique=True,
    )

    def clean(self):
        super().clean()
        letter_part = self.license_number[:3]
        digit_part = self.license_number[3:]
        if len(self.license_number) != 8:
            raise ValidationError(
                "Ensure that the license number is 8 symbols long"
            )

        if not letter_part.isalpha() or not letter_part.isupper():
            raise ValidationError(
                f"Ensure that the first 3 symbols of "
                f"license number are letters in UPPER CASE, not {letter_part}"
            )
        if not digit_part.isnumeric():
            raise ValidationError(
                f"Ensure that the symbols from 4th to 8th of "
                f"license number are digits, not {digit_part}"
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
