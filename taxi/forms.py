from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self,):
        license_number = self.cleaned_data["license_number"]
        length_license = 8
        first_three_letters = license_number[:3]
        second_five_number = license_number[3:]

        if len(license_number) != length_license:
            raise ValidationError(
                f"License number must consists only of"
                f" {length_license} characters!"
            )

        if first_three_letters != first_three_letters.upper() or \
                not all(number.isalpha() for number in first_three_letters):
            raise ValidationError(
                "License number must has First 3 characters"
                " are uppercase letters!"
            )

        if not second_five_number.isdigit():
            raise ValidationError(
                "License number must has Last 5 characters are digits"
            )
        return license_number


class CreateDriverFormView(UserCreationForm):

    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )
