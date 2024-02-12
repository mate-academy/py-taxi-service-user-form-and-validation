from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(ModelForm):
    CORRECT_LENGTH_OF_LICENSE = 8

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != self.CORRECT_LENGTH_OF_LICENSE:
            raise ValidationError("The length of license number is incorrect.")
        if (not license_number[:3].isupper()
                or not license_number[:3].isalpha()):
            raise ValidationError(
                "The first three characters should be uppercase.")
        if not license_number[3:].isdigit():
            raise ValidationError("The last five characters should be number")
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
