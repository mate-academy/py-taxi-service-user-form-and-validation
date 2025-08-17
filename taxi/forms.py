import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseNumberCleanMixin(forms.Form):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"].strip().upper()
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError(
                "License number must be in format:"
                " 3 uppercase letters + 5 digits (for example: ABC12345)")
        return license_number


class DriverCreationForm(LicenseNumberCleanMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(LicenseNumberCleanMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Car
        fields = "__all__"
