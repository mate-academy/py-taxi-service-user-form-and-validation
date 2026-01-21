from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        part1 = license_number[:3]
        part2 = license_number[3:]
        if len(license_number) != 8:
            raise ValidationError("Consist only of 8 characters")
        elif not str(part1).isalpha() or not str(part1).isupper():
            raise ValidationError("First 3 characters are uppercase letters")
        elif not part2.isdigit():
            raise ValidationError("Last 5 characters are digits")
        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseValidationMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm, DriverLicenseValidationMixin):

    class Meta:
        model = Driver
        fields = ("license_number",)
