from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverValidateMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters long"
            )
        if (
            license_number[:3].upper() != license_number[:3]
            or license_number[:3].isalpha() is False
        ):
            raise forms.ValidationError(
                "License number must be in format AAA12345"
            )
        if license_number[3:].isdigit() is False:
            raise forms.ValidationError(
                "License number must be in format AAA12345"
            )
        return license_number


class DriverCreationForm(UserCreationForm, DriverValidateMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm, DriverValidateMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer",)
