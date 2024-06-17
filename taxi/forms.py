from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


from taxi.models import Driver, Car


class DriverUserCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise (
                forms.ValidationError(
                    "License_number must be 8 characters long"
                )
            )
        if not license_number[0:3].isupper() \
                or not license_number[:3].isalpha():
            raise (
                forms.ValidationError(
                    "The first 3 characters must be uppercase letters."
                )
            )
        if not license_number[3:].isdigit():
            raise (
                forms.ValidationError("The last 5 characters must be digits.")
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
