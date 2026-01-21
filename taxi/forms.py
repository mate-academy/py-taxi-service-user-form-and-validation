import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class BaseDriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        pattern = re.compile(r"^[A-Z]{3}\d{5}$")

        if not pattern.match(license_number):
            raise forms.ValidationError(
                """
                License number must be 8 characters long and
                follow the pattern:
                First 3 characters must be uppercase letters
                and last 5 characters must be digits.
                """)

        return license_number


class DriverCreateForm(BaseDriverForm, UserCreationForm):
    class Meta(BaseDriverForm.Meta):
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(BaseDriverForm):
    pass


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
