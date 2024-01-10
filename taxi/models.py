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
    license_number = models.CharField(max_length=8, unique=True)

    def license_validation(self):
        if not self.license_number[:3].isupper():
            raise ValidationError(
                {
                    "license_number":
                        "The first three characters must be uppercase letters."
                }
            )
        if not self.license_number[-5:].isnumeric():
            raise ValidationError(
                {"license_number": "Last 5 characters must be digits."}
            )
        if len(self.license_number) != 8:
            raise ValidationError(
                {"license_number": "Should consist only of 8 characters."}
            )
        return self.license_number

    def save(self, *args, **kwargs):
        self.license_validation()
        super().save(*args, **kwargs)

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
