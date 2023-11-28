from django import forms

from taxi.models import Driver, Car
from taxi.validators import FirstCharactersUppercase, LastCharactersDigits


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        min_length=8,
        max_length=8,
        validators=[FirstCharactersUppercase(3), LastCharactersDigits(5)]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            'drivers': forms.CheckboxSelectMultiple,
        }
