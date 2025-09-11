from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ("username", "first_name", "last_name", "license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters long"
            )
        if not license_number[:3].isupper():
            raise forms.ValidationError(
                "First three characters must be uppercase"
            )
        if not license_number[-5:].isdigit():
            raise forms.ValidationError("Last five characters must be digits")

        return license_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
