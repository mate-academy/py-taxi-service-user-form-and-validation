from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError("Lenth is wrong!")
        if not (license_number[:3].isupper() and license_number[:3].isalpha()):
            raise forms.ValidationError("First 3 letter must be Uppercase!")
        if not license_number[-5:].isdigit():
            raise forms.ValidationError("Last 5 letter must be Numeric!")
        return license_number


class DriverLicenseUpdateForm(LicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(LicenseValidationMixin, UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )
