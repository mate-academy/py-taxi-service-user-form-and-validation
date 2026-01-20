from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import BaseModelForm

from taxi.models import Driver, Car


def license_number_validation(form_instance: BaseModelForm) -> str | None:
    license_number = form_instance.cleaned_data["license_number"]
    if (
        len(license_number) != 8
        or license_number[:3] != license_number[:3].upper()
        or not license_number[:3].isalpha()
        or not license_number[3:].isnumeric()
    ):
        raise ValidationError("Please, enter correct license number!")

    return license_number


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField()

    def clean_license_number(self):
        return license_number_validation(self)

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField()

    def clean_license_number(self):
        return license_number_validation(self)

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
