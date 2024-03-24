from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car
from django.forms import (
    ModelForm,
    Form,
    ModelMultipleChoiceField,
    CheckboxSelectMultiple,
)


class DriverLicenseValidation(Form):

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "Insure that the license number is 8 characters long")
        if (not license_number[0:3].isalpha()
                or not license_number[0:3].isupper()):
            raise ValidationError(
                "License number should start with 3 big letters")
        if not license_number[3:].isnumeric():
            raise ValidationError(
                "License number should ends with 5 numbers")
        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseValidation):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(ModelForm, DriverLicenseValidation):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(ModelForm):
    drivers = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
