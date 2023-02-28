from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "Ensure that your license number consist of 8 characters"
            )
        if not license_number[:3].isalpha() & license_number[:3].isupper():
            raise ValidationError(
                "Ensure that your license number "
                "starts with 3 uppercase letters"
            )
        if not license_number[3:].isnumeric():
            raise ValidationError("Check that last 5 characters are digits")
        return license_number

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


# class CarDriversUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Car
#         fields = ("drivers",)
