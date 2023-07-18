from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class BaseDriverValidationForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("License number must consist "
                                  "only of 8 characters!")

        series = license_number[:3]
        if series.upper() != series or not series.isalpha():
            raise ValidationError("The first 3 characters of license number"
                                  " must consist of uppercase letters!")

        number = license_number[3:]
        if not number.isdigit():
            raise ValidationError("The last 5 characters of license number"
                                  " must consist of digits!")

        return license_number


class DriverCreationForm(BaseDriverValidationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",
                                                 "first_name",
                                                 "last_name")


class DriverLicenseUpdateForm(BaseDriverValidationForm):

    class Meta(BaseDriverValidationForm):
        model = Driver
        fields = ("license_number",)
