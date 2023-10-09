from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from taxi.models import Driver, Car


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must contain 8 characters"
            )

        if not (license_number[:3].isupper() and license_number[:3].isalpha()):
            raise forms.ValidationError(
                "License number must start with 3 uppercase letters"
            )

        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "License number must end with 5 digits"
            )

        return license_number


class DriverCreateForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Car
        fields = "__all__"
