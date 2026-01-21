from django import forms

from .models import Driver, Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise forms.ValidationError("License number must"
                                    " be exactly 8 characters long.")

    if not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise forms.ValidationError("The first 3 "
                                    "characters must be uppercase letters.")

    if not license_number[3:].isdigit():
        raise forms.ValidationError("The last 5 characters must be digits.")

    return license_number


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        return validate_license_number(license_number)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Car
        fields = "__all__"
