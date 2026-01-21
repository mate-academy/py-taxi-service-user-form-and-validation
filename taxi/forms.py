from django import forms
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError("License number must be 8 symbols")
        elif not license_number[0:2].isalpha() or not license_number[2::].isdigit():
            raise forms.ValidationError("Please enter a valid number")
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Car
        fields = "__all__"