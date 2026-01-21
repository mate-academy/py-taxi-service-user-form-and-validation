import re
from django import forms
from django.contrib.auth.password_validation import validate_password
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
    license_number = models.CharField(max_length=255, unique=True)

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


def validate_license_format(value):

    if not re.fullmatch(r'[A-Z]{3}\d{5}', value):
        raise ValidationError(
            'License must be 3 uppercase letters followed by 5 digits (e.g. ABC23456).',
            code='invalid_license'
        )

class DriverForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        validators=[validate_password],
        help_text=('Your password must be at least 8 characters, '
                   'not too common, and not entirely numeric.')
    )
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_format],
        help_text='3 letters + 5 digits, e.g. ABC23456'
    )

    class Meta:
        model = Driver
        fields = [
            'username', 'password', 'email',
            'first_name', 'last_name', 'license_number'
        ]

class DriverUpdateForm(forms.ModelForm):
    # Re-use your license validator:
    license_number = forms.CharField(
        max_length=8,
        validators=[validate_license_format],
        help_text='3 letters + 5 digits, e.g. ABC23456'
    )

    class Meta:
        model = Driver
        fields = ['email', 'license_number']
        widgets = {
            'email': forms.EmailInput(attrs={'autocomplete': 'email'}),
        }