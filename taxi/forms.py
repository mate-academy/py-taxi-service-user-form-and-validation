from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(max_length=8)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters"
            )

        if not (
            license_number[:3].isalpha()
            and license_number[:3].isupper()
            and license_number[3:].isdigit()
        ):
            raise forms.ValidationError(
                "License number must be 3 uppercase letters and 5 digits"
            )

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters"
            )

        if not (
            license_number[:3].isalpha()
            and license_number[:3].isupper()
            and license_number[3:].isdigit()
        ):
            raise forms.ValidationError(
                "License number must be 3 uppercase letters and 5 digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
