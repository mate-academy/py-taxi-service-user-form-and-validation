from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from taxi.models import Car, Driver


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self) -> None:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8 or\
                not license_number[:3].isalpha() or\
                not license_number[:3].isupper() or\
                not license_number[3:].isdigit():
            raise ValidationError("Driver license must be 8 characters long,\
                                   with the first 3 characters as uppercase\
                                   letters and the last 5 as digits")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> None:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8 or\
                not license_number[:3].isalpha() or\
                not license_number[:3].isupper() or\
                not license_number[3:].isdigit():
            raise ValidationError("Driver license must be 8 characters long,\
                                   with the first 3 characters as uppercase\
                                   letters and the last 5 as digits")
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
