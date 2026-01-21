from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]


class LicenseNumberMixin(forms.Form):
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "Driver's license number must consist of exactly 8 characters."
            )

        if (not license_number[:3].isupper()
                or not license_number[:3].isalpha()):
            raise forms.ValidationError(
                "First 3 characters of the license number"
                "must be uppercase letters."
            )

        if not license_number[-5:].isdigit():
            raise forms.ValidationError(
                "Last 5 characters of the license number must be digits"
            )

        return license_number


class DriverCreationForm(UserCreationForm, LicenseNumberMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (
            UserCreationForm.Meta.fields
            + ("first_name", "last_name", "license_number",)
        )


class DriverLicenseUpdateForm(forms.ModelForm, LicenseNumberMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)
