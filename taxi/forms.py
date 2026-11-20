from django import forms
from .models import Driver, Car

def validate_license_number(value):
    if len(value) != 8:
        raise forms.ValidationError("A licença deve conter 8 caracteres.")
    if not value[:3].isalpha() or not value[:3].isupper():
        raise forms.ValidationError("Os 3 primeiros caracteres devem ser letras maiúsculas."
        )
    if not value[3:].isdigit():
        raise forms.ValidationError("Os 5 últimos caracteres devem ser números."
        )
    return value

class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError(
            )
        if not license_number[:3].isupper():
            raise forms.ValidationError(
            )
        if not license_number[:3].isalpha():
            raise forms.ValidationError(
            )
        if not license_number[3:].isdigit():
            raise forms.ValidationError(
            )
        return validate_license_number(self.cleaned_data['license_number'])

class DriverCreationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
        )
    def clean_license_number(self):
        return validate_license_number(
            self.cleaned_data["license_number"]
        )

class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Car
        fields = (
            "model",
            "manufacturer",
            "drivers",
        )
