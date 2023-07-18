from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENCE_LENGTH = 8
    DIGIT = 5
    CHARS = 3

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.LICENCE_LENGTH:
            raise ValidationError(
                f"The licence should consist with"
                f" {self.LICENCE_LENGTH} symbols"
            )
        if not (license_number[:self.CHARS].isupper()
                and license_number[:self.CHARS].isalpha()):
            raise ValidationError(
                f"The first {self.CHARS}"
                f" characters should be uppercase letters"
            )
        if not license_number[self.CHARS:].isdigit():
            raise ValidationError(
                f"The last {self.DIGIT} characters should be digits"
            )
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
