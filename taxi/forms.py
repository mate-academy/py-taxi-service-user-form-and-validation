from django import forms
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        label="License number",
        help_text="Consists of exactly 8 characters: "
                  "First 3 characters are uppercase letters, "
                  "Last 5 characters are digits",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}[0-9]{5}$",
                message="The license number must consist "
                        "of exactly 3 capital letters followed by 5 digits.",
            )
        ],
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
