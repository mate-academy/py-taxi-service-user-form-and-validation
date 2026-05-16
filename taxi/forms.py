from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError("Wrong license length")
        prefix = license_number[:3]
        if not prefix.isalpha() or not prefix.isupper():
            raise forms.ValidationError("Invalid started letters")
        if not license_number[3:].isdigit():
            raise forms.ValidationError("Wrong license number")
        return license_number


class DriverCreateForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = (
            UserCreationForm.Meta.fields
            + ("first_name", "last_name", "license_number", "email")
        )

    def clean_license_number(self):
        license_number = DriverLicenseUpdateForm.clean_license_number(self)
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
