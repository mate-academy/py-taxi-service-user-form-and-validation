from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Driver, Car, Manufacturer


UserModel = get_user_model()


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENCE_NUMBER_LENGTH = 8

    class Meta:
        model = UserModel
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if len(license_number) != self.LICENCE_NUMBER_LENGTH:
            raise forms.ValidationError(
                f"License number must be exactly "
                f"{self.LICENCE_NUMBER_LENGTH} characters long."
            )
        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise forms.ValidationError(
                "The first three characters must be uppercase letters."
            )
        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "The last five characters must be digits."
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=UserModel.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
