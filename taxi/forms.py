from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name", "email"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters long"
            )
        elif not (
                license_number[:3].isupper() and license_number[:3].isalpha()
        ):
            raise forms.ValidationError(
                "First 3 characters of the license "
                "number must be uppercase letters"
            )
        elif not license_number[3:].isdigit():
            raise forms.ValidationError(
                "Last 5 characters license number must be digits"
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta(UserCreationForm.Meta):
        model = Car
        fields = "__all__"
