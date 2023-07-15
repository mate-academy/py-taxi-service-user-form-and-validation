from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError


from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_NUMBER_LENGTH = 8
    QUANTITY_LETTERS = 3
    QUANTITY_DIGITS = 5

    class Meta:
        model = get_user_model()
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not len(license_number) == self.LICENSE_NUMBER_LENGTH:
            raise ValidationError("Consist only of 8 characters")

        elif not (
                license_number[:self.QUANTITY_LETTERS].isalpha() and
                license_number[:self.QUANTITY_LETTERS].isupper()
        ):
            raise ValidationError("First 3 characters should be uppercase letters")

        elif not license_number[-self.QUANTITY_DIGITS:].isdigit():
            raise ValidationError("Last 5 characters should be digits")
        return license_number


class CreateCarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
