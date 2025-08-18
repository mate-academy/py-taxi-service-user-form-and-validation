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

    class Meta:
        verbose_name = "driver"
        verbose_name_plural = "drivers"

    def clean(self):
        number = self.license_number
        if not number:
            raise ValidationError("License number is required.")
        if Driver.objects.filter(
                license_number=number
        ).exclude(pk=self.pk).exists():
            raise ValidationError("This license number is already in use.")
        elif len(number) != 8:
            raise ValidationError("License number must be 8 digits.")
        letters, digits = number[:3], number[3:]
        if not letters.isupper() or not letters.isalpha():
            raise ValidationError(
                "License number must start with uppercase letters."
            )
        if not digits.isdigit():
            raise ValidationError("License number must contain digits.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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
