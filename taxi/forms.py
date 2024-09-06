from django import forms
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car

LEN_LICENSE_CHARS = 8


def check_license_number(licence_number):
    if len(licence_number) != LEN_LICENSE_CHARS:
        raise forms.ValidationError(
            f"Ensure that value len is {LEN_LICENSE_CHARS}"
        )
    if not licence_number[-5:].isdigit():
        raise forms.ValidationError(
            "Ensure that licence numbers write correct"
        )
    if not licence_number[:3].isupper() or not licence_number[:3].isalpha():
        raise forms.ValidationError(
            "Ensure that licence chars write correct"
        )
    return licence_number


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        return check_license_number(self.cleaned_data["license_number"])


class DriverCreateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = "__all__"

    def clean_license_number(self):
        return check_license_number(self.cleaned_data["license_number"])


class DriverUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"

    def clean_license_number(self):
        return check_license_number(self.cleaned_data["license_number"])


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
