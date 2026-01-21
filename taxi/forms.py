from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseNumberValidationMixin():

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "Make sure your license number contains 8 characters"
            )
        elif (not license_number[:3].isupper()
              or not license_number[:3].isalpha()):
            raise ValidationError(
                "First three characters should be upper letters"
            )
        elif not license_number[3:].isnumeric():
            raise ValidationError("Last five characters should be digits")
        return license_number


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
