from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("Ensure that license number has length 8")

        if not license_number[:3].isupper():
            raise ValidationError(
                "Ensure that license number first 3 symbols is upper letters"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Ensure that license number last 5 symbols is digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Driver.objects.all(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
