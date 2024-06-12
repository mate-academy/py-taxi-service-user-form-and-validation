from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Driver
        fields = (("first_name", "last_name", "email")
                  + ("license_number", "username", ))

    def clean_license_number(self) -> object:
        license_number = self.cleaned_data["license_number"]
        error = ("Must be 8 characters. "
                 "First 3 characters must be uppercase letters. "
                 "Last 5 characters must be digits")
        if len(license_number) == 8 and (license_number[:3].isupper()
                                         and license_number[:3].isalpha()
                                         and license_number[3:].isdigit()):
            return license_number
        raise forms.ValidationError(error)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self) -> object:
        license_number = self.cleaned_data["license_number"]
        error = ("Must be 8 characters. "
                 "First 3 characters must be uppercase letters. "
                 "Last 5 characters must be digits")
        if (len(license_number) == 8 and (license_number[:3].isupper()
                                          and license_number[:3].isalpha()
                                          and license_number[3:].isdigit())):
            return license_number
        else:
            raise forms.ValidationError(error)
