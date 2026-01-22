from django import forms
from django.contrib.auth.forms import UserCreationForm
from taxi.models import Car, Driver


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "Ensure that license_number has only 8 symbols"
            )
        if (
            not license_number[:3].isalpha()
            or not license_number[:3].isupper()
            or not license_number[3:].isdigit()
        ):
            raise forms.ValidationError(
                "Ensure that license_number start with 3 UPPER"
                " symbols and last 5 characters are digits"
            )

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "Ensure that license_number has only 8 symbols"
            )
        if (
            not license_number[:3].isalpha()
            or not license_number[:3].isupper()
            or not license_number[3:].isdigit()
        ):
            raise forms.ValidationError(
                "Ensure that license_number start with 3 UPPER symbols"
                " and last 5 characters are digits"
            )

        return license_number


class CarCreationForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
