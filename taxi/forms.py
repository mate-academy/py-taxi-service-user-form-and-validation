import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "License must have 3 uppercase letters"
                " followed by 5 digits, e.g. ABC12345."
            )

        if (Driver.objects.filter(license_number=license_number).
                exclude(pk=self.instance.pk).exists()):
            raise forms.ValidationError(
                "This license number is already in use."
            )

        return license_number


class DriverLicenseUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise forms.ValidationError(
                "License must have 3 uppercase letters"
                " followed by 5 digits, e.g. ABC12345."
            )

        if (Driver.objects.filter(license_number=license_number).
                exclude(pk=self.instance.pk).exists()):
            raise forms.ValidationError(
                "This license number is already in use."
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
