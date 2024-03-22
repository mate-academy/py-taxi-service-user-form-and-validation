from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            "license_number",
        ]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        length = 8

        if len(license_number) < length:
            raise ValidationError(
                f"License number must be {length} characters long"
            )

        if not (license_number[:3].isupper() and license_number[:3].isalpha()):
            raise ValidationError("Three first letters must be in uppercase")

        if not license_number[-5:].isdigit():
            raise ValidationError("Last 5 characters must be digits")

        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = (
            "model",
            "manufacturer",
        )
