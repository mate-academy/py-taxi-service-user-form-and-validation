from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCretionForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name",
                                                 "last_name",
                                                 "license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        license_up_alph = license_number[:3]

        if len(license_number) != 8 or not license_number.isidentifier():
            raise ValidationError(
                "Should contain 8 symbols(digits and letters)"
            )
        if not license_number[3:].isdigit():
            raise ValidationError("License number should contain 5 digits")
        if not license_up_alph.isupper() or not license_up_alph.isalpha():
            raise ValidationError(
                "License number should contain 3 UPPERCASE letters "
            )

        return license_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers",)
