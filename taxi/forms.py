from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LENGTH:
            raise ValidationError(f"License number should be {self.LENGTH}")

        if not (license_number[:3].isupper() and license_number[:3].isalpha()):
            raise ValidationError("First 3 characters should be capitalize")

        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters should be digits")

        return license_number


class DriverCreateForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )

    def clean_license_number(self):
        return super().clean_license_number()


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
