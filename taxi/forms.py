from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Driver, Car


class CleanLicenseNumberMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "license_number must be 8 characters long")
        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise forms.ValidationError(
                "incorrect license number template "
                "first 3 characters must be uppercase")
        if not license_number[-5:].isdigit():
            raise forms.ValidationError("incorrect license number template,"
                                        "last 5 digits allowed")
        return license_number


class DriverForm(UserCreationForm,
                 CleanLicenseNumberMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name",
                                                 "last_name",
                                                 "license_number",)


class DriverLicenseUpdateForm(forms.ModelForm,
                              CleanLicenseNumberMixin):
    class Meta:
        model = Driver
        fields = ["license_number", ]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
