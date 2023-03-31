from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    cons = Driver.license_number

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        number = self.cleaned_data["license_number"]

        if len(number) != 8:
            raise ValidationError(
                "The length of the license number is not correct"
            )
        if not number[:3].isupper() or not number[:3].isalpha():
            raise ValidationError(
                "The first three characters must be uppercase"
            )
        if not number[3:].isdigit():
            raise ValidationError(
                "The last five characters must be digits"
            )

        return number


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name"
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
