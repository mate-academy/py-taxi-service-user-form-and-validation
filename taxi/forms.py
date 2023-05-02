from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    MIN_CHARACTER = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.MIN_CHARACTER:
            raise ValidationError(
                f"Ensure that license consist only of "
                f"{self.MIN_CHARACTER} characters"
            )
        elif not license_number[-5:].isdigit():
            raise ValidationError("last 5 characters should be digit")
        elif not license_number[:3].isalpha() or license_number[:3].islower():
            raise ValidationError(
                "first 3 character should be uppercase letters"
            )

        return license_number


class DriverCreationForm(UserCreationForm, DriverLicenseUpdateForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )

    def clean_license_number(self):
        return super().clean_license_number()


class CarForm(UserCreationForm.Meta):
    model = Car
    fields = "__all__"


# class AssignRemoveForm(forms.ModelForm):
#     class Meta:
#         model = Car
#         fields = ()