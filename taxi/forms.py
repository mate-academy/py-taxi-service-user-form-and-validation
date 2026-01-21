from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.mixins import LicenseNumberValidationMixin
from taxi.models import Driver, Car


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("license_number", "username", "first_name", "last_name",))

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        return self.validate_license_number(license_number)


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        return self.validate_license_number(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Car
        fields = "__all__"
