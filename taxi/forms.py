from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseNumberMixin:
    def clean_license_number(self):
        data = self.cleaned_data.get("license_number")

        if data:
            if len(data) != 8:
                raise ValidationError(
                    "License number must consist of 8 characters"
                )

            if not data[:3].isupper():
                raise ValidationError(
                    "The first 3 characters must be uppercase"
                )

            if not data[:3].isalpha():
                raise ValidationError(
                    "The first 3 characters must be letters"
                )

            if not data[3:].isdigit():
                raise ValidationError(
                    "The last 5 characters must be digits"
                )

        return data


class DriverCreateForm(LicenseNumberMixin, UserCreationForm):
    license_number = forms.CharField(
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name",
        )


class DriverLicenseUpdateForm(LicenseNumberMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)
        widgets = {
            "license_number": forms.TextInput(
                attrs={
                    "placeholder": "Enter a license number"
                }
            )
        }


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
