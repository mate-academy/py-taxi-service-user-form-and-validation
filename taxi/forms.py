from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):

    first_name = forms.CharField(max_length=63, required=True)
    last_name = forms.CharField(max_length=63, required=True)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        should_be_upper_chars = license_number[:3]
        should_be_digits = license_number[3:]

        if len(license_number) != 8:
            raise forms.ValidationError("Ensure this value has 8 characters.")

        if not (
            all([should_be_upper_chars.isalpha(),
                 should_be_upper_chars.isupper()])
        ):
            raise forms.ValidationError(
                "First 3 characters should be uppercase letters."
            )

        if not (should_be_digits.isdigit()):
            raise forms.ValidationError("Last 5 characters should be digits.")

        return license_number
