from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License number must be at least 8 digits")
        elif not license_number[:3].isupper():
            raise ValidationError(
                "First 3 character must be a uppercase letter"
            )
        elif not license_number[3:].isnumeric():
            raise ValidationError("Last 5 characters must be a digits")


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License number must be at least 8 digits")
        elif not license_number[:3].isupper():
            raise ValidationError(
                "First 3 character must be a uppercase letter"
            )
        elif not license_number[3:].isnumeric():
            raise ValidationError("Last 5 characters must be a digits")


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
