from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from taxi.models import Car

User = get_user_model()


class DriverLicenseValidationMixin:

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if license_number is None or len(license_number) != 8:
            raise ValidationError("License number is invalid")
        if (not license_number[:3].isalpha()
                or license_number[:3].upper() != license_number[:3]):
            raise ValidationError("License number is invalid")
        if not license_number[3:].isnumeric() or len(license_number[3:]) != 5:
            raise ValidationError("License number is invalid")
        return license_number


class DriverCreationForm(DriverLicenseValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number",))


class DriverLicenseUpdateForm(DriverLicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "license_number",)


class CarCreationFrom(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
