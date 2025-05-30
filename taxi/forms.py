from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator, RegexValidator

from .models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                regex=r"^[A-Z]{3}[0-9]{5}$",
                message="Please enter a valid license number."
            )
        ]
    )

    class Meta(forms.ModelForm):
        model = Driver
        fields = ["license_number", ]


class DriverCreateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                regex=r"^[A-Z]{3}[0-9]{5}$",
                message="Please enter a valid license number."
            )
        ]
    )

    class Meta(forms.ModelForm):
        model = Driver
        fields = "__all__"


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
