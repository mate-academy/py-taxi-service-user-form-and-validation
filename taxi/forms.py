from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}[0-9]{5}$",
                message="Please enter a valid license number.(AAA00000)"
            )
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "Invalid license number. "
                "License number need to have 8 symbols."
            )

        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise ValidationError(
                "Invalid license number. "
                "License number should have 3 upper letters."
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Invalid license number. "
                "License number should have 5 numbers."
            )

        return license_number
