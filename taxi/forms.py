from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseNumberValidationMixin(forms.ModelForm):
    LENGTH = 8
    FIRST_SYMBOL = 3
    LAST_SYMBOL = -5

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != self.LENGTH:
            raise forms.ValidationError(
                f"Length of license number must be {self.LENGTH}"
            )
        if (license_number[:self.FIRST_SYMBOL]
                != license_number[:self.FIRST_SYMBOL].upper()):
            raise forms.ValidationError(
                "First 3 symbol must be letters in uppercase"
            )
        if not license_number[:self.FIRST_SYMBOL].isalpha():
            raise forms.ValidationError("First 3 symbol must be letter")
        if not license_number[self.LAST_SYMBOL:].isdigit():
            raise forms.ValidationError("Last 5 symbol must be digits")
        return license_number


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
