import re
from django.contrib.auth.forms import UserCreationForm
from django import forms
from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if not re.fullmatch(r"[A-Z]{3}[0-9]{5}", license_number):
            raise forms.ValidationError(
                "License number must have 3 uppercase letters followed by 5 digits."
            )
        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "license_number")

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if not re.fullmatch(r"[A-Z]{3}[0-9]{5}", license_number):
            raise forms.ValidationError(
                "License number must have 3 uppercase letters followed by 5 digits."
            )
        return license_number

class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
