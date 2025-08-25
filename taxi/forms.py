from django import forms

from .models import Driver, Car, Manufacturer


class DriverLicenseUpdateForm(forms.ModelForm):

    LICENCE_NUMBER_LENGTH = 8

    class Meta:
        model = Driver
        fields = ['license_number']

    def clean_license_number(self):
        license_number = self.cleaned_data.get('license_number')
        if not len(license_number) == self.LICENCE_NUMBER_LENGTH:
            raise forms.ValidationError(
                f"License number must be exactly "
                f"{self.LICENCE_NUMBER_LENGTH} characters long."
            )
        if not license_number[:3] == license_number[:3].upper():
            raise forms.ValidationError(
                "The first three characters must be uppercase letters."
            )
        if not license_number[5:].isdigit():
            raise forms.ValidationError(
                "The last three characters must be digits."
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
