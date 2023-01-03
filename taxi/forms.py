from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car, Manufacturer


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "password", "first_name", "last_name", "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = str(self.cleaned_data["license_number"])

        if len(license_number) != 8 or \
                not license_number[:3].isupper() or \
                not license_number[:3].isalpha() or \
                not license_number[-5:].isdigit():
            raise ValidationError("License number is invalid")

        return license_number
