from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Car
import re


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        value = self.cleaned_data.get("license_number", "")

        pattern = r"^[A-Z]{3}\d{5}$"

        if not re.match(pattern, value):
            raise forms.ValidationError(
                "License number must have 3 uppercase letters followed by 5 digits. "
                "Example: ABC12345"
            )

        return value


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class DriverAddForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
