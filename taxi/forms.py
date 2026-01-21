from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverLicenseValidationMixin(forms.BaseForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "The length of the license number must be 8 characters."
            )

        series, number = license_number[:3], license_number[3:]

        if not series.isalpha() or not series.isupper():
            raise forms.ValidationError(
                "Driver's license series does not match the expected format"
            )

        if not number.isdigit():
            raise forms.ValidationError(
                "Driver's license number must contain only digits."
            )

        return license_number


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
