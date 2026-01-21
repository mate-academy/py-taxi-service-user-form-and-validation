from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from taxi.models import Car, Driver


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}[0-9]{5}$",
                message="License number must be 3 uppercase"
                        " letters followed by 5 digits"
                        " (e.g. 'ABC12345')."
            )
        ],
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
