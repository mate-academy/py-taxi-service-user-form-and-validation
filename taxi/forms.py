from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_NUMBER_LENGTH = 8
    LICENSE_NUMBER_LETTER_PART = 3
    LICENSE_NUMBER_DIGIT_PART = 5

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LICENSE_NUMBER_LENGTH:
            raise ValidationError(
                "License numbers consist of "
                f"{self.LICENSE_NUMBER_LENGTH} characters!"
            )

        for char in license_number[:self.LICENSE_NUMBER_LETTER_PART]:
            if not char.isalpha() or not char.isupper():
                raise ValidationError(
                    f"Ensure that first {self.LICENSE_NUMBER_LETTER_PART} "
                    "characters are uppercase letters!"
                )

        for char in license_number[self.LICENSE_NUMBER_LETTER_PART:]:
            if not char.isdigit():
                raise ValidationError(
                    "Ensure that last "
                    f"{self.LICENSE_NUMBER_DIGIT_PART} "
                    "characters are digits!"
                )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
