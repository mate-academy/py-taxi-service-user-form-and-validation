from django import forms
from django.core.exceptions import ValidationError
from .models import Driver, Car

class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['license_number']

    def clean_license_number(self):
        license_number = self.cleaned_data['license_number']
        if len(license_number) != 8:
            raise ValidationError("Numer prawa jazdy musi składać się z 8 znaków.")

        if not license_number[:3].isalpha() or not license_number[:3].isupper():
            raise ValidationError("Pierwsze 3 znaki muszą być dużymi literami.")

        if not license_number[3:].isdigit():
            raise ValidationError("Ostatnie 5 znaków muszą być cyframi.")

        return license_number

class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'drivers']
