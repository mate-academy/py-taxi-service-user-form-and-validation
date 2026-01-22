from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
            "email"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        print(license_number[3:], license_number[:3])
        if len(license_number) != self.LICENSE_LENGTH:
            raise ValidationError("length of license number must be 8")
        if (
                not license_number[3:].isnumeric()
                or not license_number[:3].isalpha()
        ):
            raise ValidationError("license number must end with 5 digits")
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


class CarDetailForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = "__all__"
