from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from config import constant
from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number")


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(required=True, validators=[])

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not len(license_number) == constant.LEN_LICENSE_NUMBER:
            raise ValidationError(
                f"license number must be {constant.LEN_LICENSE_NUMBER} "
                f"characters long")
        if not (license_number[0:3].isupper()
                and license_number[0:3].isalpha()):
            raise ValidationError(
                "First 3 characters must be capital letters")
        if not license_number[-5:].isdigit():
            raise ValidationError(
                "The last five characters must be digits")
        return license_number


class CarForm(forms.ModelForm):
    cars = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", )
        label = "drivers"
