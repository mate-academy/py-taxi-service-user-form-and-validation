from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not (
            len(license_number) == 8
            and license_number[:3].isupper()
            and license_number[:3].isalpha()
            and license_number[3:].isdigit()
        ):

            raise forms.ValidationError("Invalid license number")

        return license_number


class DriverForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)
