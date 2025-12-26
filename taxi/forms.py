from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(forms.ModelForm):
    CORRECT_AMOUNT = 8

    license_number = forms.CharField(max_length=CORRECT_AMOUNT)

    class Meta:
        model = Driver
        fields = (
            "license_number",
            "first_name",
            "last_name",
            "email",
            "username",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverCreationForm.CORRECT_AMOUNT:
            raise ValidationError("Invalid length of license number")
        elif license_number[:3] != license_number[:3].upper():
            raise ValidationError(
                "First 3 letters should be uppercase letters"
            )
        elif not license_number[-5:].isdigit():
            raise ValidationError("Last 5 symbols should be numbers")
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
