from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def validate_license_number(value: str):
    if len(value) != 8:
        raise ValidationError(
            _("%(value)s is not 8 characters long"),
            params={"value": value}
        )
    if not value[:3].isupper() or not value[:3].isalpha():
        raise ValidationError(
            _("first 3 characters should be uppercase letters")
        )
    if not value[-5:].isnumeric():
        raise ValidationError(
            _("last 5 characters should be digits")
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
        max_length=255,
        unique=True,
        validators=[validate_license_number]
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
