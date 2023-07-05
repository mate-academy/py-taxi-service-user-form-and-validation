from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name")


class DriverLicenseUpdateForm(forms.ModelForm):
    LEN_OF_LICENSE_NUMBER = 8
    INDEX_OF_CHARACTERS = 3

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != self.LEN_OF_LICENSE_NUMBER:
            raise ValidationError(f"Length of driver license should be equal {self.LEN_OF_LICENSE_NUMBER}")
        if not (
                license_number[:self.INDEX_OF_CHARACTERS].isupper()
        ) or not (
                license_number[:self.INDEX_OF_CHARACTERS].isalpha()
        ):
            raise ValidationError("First 3 characters should be uppercase letters")
        if not license_number[self.INDEX_OF_CHARACTERS:].isnumeric():
            raise ValidationError("Last 5 characters should be digits")
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
