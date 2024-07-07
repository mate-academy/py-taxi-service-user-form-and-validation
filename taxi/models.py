from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
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
        max_length=255, unique=True,
    )

    def clean(self, *args, **kwargs):
        if len(self.license_number) != 8:
            raise ValidationError("license number must be 8")
        if not (self.license_number[:3].isupper()
                and self.license_number[:3].isalpha()):
            raise ValidationError("first 3 characters should be in upper case")
        if not (self.license_number[3:].isdigit()):
            raise ValidationError("last 5 characters should be digits")

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
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

    def get_absolute_url(self):
        return reverse("taxi:car-detail", kwargs={"pk": self.pk})
