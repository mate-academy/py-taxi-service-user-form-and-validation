from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.exceptions import ValidationError


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


class Driver(AbstractUser):
    license_number = models.CharField(max_length=255, unique=True)

    def clean(self):
        super().clean()
        self.validate_license_number()

    def validate_license_number(self):
        license_number = str(self.license_number)
        if len(license_number) != 8:
            raise ValidationError("Licence number must be 8 characters long")
        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise ValidationError(
                "Licence number must have 3 first uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError("Licence number must have 5 last digits")

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
