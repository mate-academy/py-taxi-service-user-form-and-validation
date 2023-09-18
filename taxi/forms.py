from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("username", "license_number")


class CarForm(forms.ModelForm):
    cars = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.Form):
    license_number = forms.CharField(label="License Number", max_length=8)

    def clean_license_number(self) -> None:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must consist of exactly 8 characters."
            )
        if not license_number[:3].isalpha()\
                or not license_number[:3].isupper():
            raise forms.ValidationError(
                "First 3 characters of the license number"
                " must be uppercase letters."
            )
        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "Last 5 characters of the license number must be digits."
            )
        return license_number
