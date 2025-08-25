from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django import forms


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


class Driver(AbstractUser):

    LICENCE_NUMBER_LENGTH = 8

    license_number = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{3}[0-9]{5}$',
                message=
                "License must be exactly 8 characters: "
                "first 3 uppercase letters, last 5 digits."
            )
        ])

    class Meta:
        verbose_name = "driver"
        verbose_name_plural = "drivers"


#second option to validate license number
    # def clean(self):
    #     cleaned_data = super().clean()
    #     license_number = cleaned_data.get("license_number")
    #     if license_number:
    #         if len(license_number) != 8:
    #             raise forms.ValidationError(
    #             "License number must be exactly 8 characters long."
    #             )
    #
    #         if (not license_number[:3].isalpha() or
    #         not license_number[:3].isupper()):
    #     raise forms.ValidationError(
    #         "The first three characters must be uppercase letters."
    #     )
    #             raise forms.ValidationError(
    #             "The first three characters must be uppercase letters."
    #             )
    #
    #         if not license_number[3:].isdigit():
    #             raise forms.ValidationError(
    #             "The last five characters must be digits."
    #             )
    #
    #     return license_number

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
