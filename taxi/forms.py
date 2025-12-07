from django import forms

from taxi.models import Driver, Car


class BaseDriverLicenseForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "License number must be 8 characters long."
            )

        if not (license_number[:3].isalpha()
                and license_number[:3].isupper()):
            raise forms.ValidationError(
                "The first 3 characters must be uppercase letters."
            )

        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "Last 5 characters must be digits."
            )

        return license_number


class DriverLicenseUpdateForm(BaseDriverLicenseForm):
    class Meta(BaseDriverLicenseForm.Meta):
        fields = ["license_number"]


class DriverCreateLicenseForm(BaseDriverLicenseForm):
    class Meta(BaseDriverLicenseForm.Meta):
        fields = "__all__"


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"

    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
