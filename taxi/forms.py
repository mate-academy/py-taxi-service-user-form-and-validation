from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car
from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", "first_name", "last_name")


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = str(self.cleaned_data["license_number"])
        if len(license_number) != 8:
            raise ValidationError(
                f"size of license must be 8 symbols, {len(license_number)} were given"
            )
        if not license_number[:3].isalpha() or not license_number[:3].isupper():
            raise ValidationError(
                f"First 3 characters must be uppercase letters"
            )
        if license_number[3:].isdigit() is False:
            raise ValidationError(
                f"Last 5 characters must be digits"
            )
        return license_number


class CarForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
