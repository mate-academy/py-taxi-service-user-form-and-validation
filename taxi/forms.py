from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from taxi.models import Driver, Car


def license_number_validation(license_number):
    if not len(license_number) == 8:
        raise ValidationError("The length must be 8.")
    elif not license_number[:3].isalpha() or not license_number[:3].isupper():
        raise ValidationError("Three first symbols must be uppercase letters")
    elif not license_number[-5:].isdigit():
        raise ValidationError("last 5 symbols must be digits")
    return license_number


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name",
                                                 "last_name",
                                                 "license_number", )

    def clean_license_number(self):
        return license_number_validation((self.cleaned_data["license_number"]))


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ["license_number", ]

    def clean_license_number(self):
        return license_number_validation(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Car
        fields = "__all__"
