from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverLicenseValidationMixin(forms.BaseForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not self._is_valid_length(license_number):
            raise forms.ValidationError(
                "The length of the license number must be 8 characters."
            )

        series, number = license_number[:3], license_number[3:]

        if not self._is_valid_series(series):
            raise forms.ValidationError(
                "Driver's license series does not match the expected format"
            )

        if not self._is_valid_number(number):
            raise forms.ValidationError(
                "Driver's license number must contain only digits."
            )

        return license_number

    def _is_valid_length(self, license_number):
        return len(license_number) == 8

    def _is_valid_series(self, series):
        return series.isalpha() and series.isupper()

    def _is_valid_number(self, number):
        return number.isdigit()


class DriverLicenseUpdateForm(DriverLicenseValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreationForm (DriverLicenseValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
