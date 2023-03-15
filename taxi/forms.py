from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm, forms.ModelForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name",)


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "Kindly endure that license_number is 8-characters long"
            )

        if not all([letter.isupper() for letter in license_number[:3]]):
            raise ValidationError(
                "Kindly ensure that first 3 characters are upper case"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Kindly ensure that last 5 characters are digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
