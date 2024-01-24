from django import forms
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if (len(license_number) != 8
                or not license_number[:3].isalpha()
                or not license_number[3:].isdigit()):
            raise forms.ValidationError("Invalid license number")
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
