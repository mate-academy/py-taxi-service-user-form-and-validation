from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[MinLengthValidator(8), MaxLengthValidator(8)],
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if license_number[:3] != license_number[:3].upper():
            raise ValidationError(
                "The first three letters must be capitalized"
            )
        elif not license_number[3:].isdigit():
            raise ValidationError(
                "The last five characters must be numbers"
            )
        elif not license_number[:3].isalpha():
            raise ValidationError(
                "The first three characters must be latin liters"
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[MinLengthValidator(8), MaxLengthValidator(8)],
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if license_number[:3] != license_number[:3].upper():
            raise ValidationError(
                "The first three letters must be capitalized"
            )
        elif not license_number[3:].isdigit():
            raise ValidationError(
                "The last five characters must be numbers"
            )
        elif not license_number[:3].isalpha():
            raise ValidationError(
                "The first three characters must be latin liters"
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
