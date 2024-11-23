from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "Ensure your license number contains 8 characters!"
            )
        elif (not license_number[:3].isalpha()
              or not license_number[:3].isupper()):
            raise ValidationError(
                "First three characters should be upper letters"
            )
        elif not license_number[3:].isnumeric():
            raise ValidationError(
                "Last five characters should be digits"
            )
        return license_number


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number",))

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "Ensure your license number contains 8 characters!"
            )
        elif (not license_number[:3].isalpha()
              or not license_number[:3].isupper()):
            raise ValidationError(
                "First three characters should be upper letters"
            )
        elif not license_number[3:].isnumeric():
            raise ValidationError(
                "Last five characters should be digits"
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
