from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseValidator:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError("Key length should be 8")

        if (license_number[:3].isalpha() is False
                or license_number[:3] != license_number[:3].upper()):
            raise forms.ValidationError("First 3 symbols"
                                        " should be uppercase Letters")

        if license_number[3:].isnumeric() is False:
            raise forms.ValidationError("Last 5 symbols"
                                        " should be digits")
        return license_number


class DriverForm(LicenseValidator, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(LicenseValidator, forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("license_number",)
