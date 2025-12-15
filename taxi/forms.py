from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm)
from django.core.exceptions import ValidationError
from django import forms
from taxi.models import Car


class LicenseValidationMixin():

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if license_number:
            if len(license_number) != 8:
                raise ValidationError(
                    "License number must contain 8 characters."
                )
            if not license_number[:3].isupper():
                raise ValidationError("First 3 characters must be uppercase.")
            if not license_number[:3].isalpha():
                raise ValidationError("First 3 characters must be letters.")
            if not license_number[3:].isdigit():
                raise ValidationError("Last 5 characters must be digits.")
            return license_number


class DriverCreationForm(LicenseValidationMixin, UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(LicenseValidationMixin, UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
