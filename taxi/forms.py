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
        )


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        license_number_alpha = license_number[:3]
        license_number_num = license_number[3:]

        if not len(license_number) == 8:
            raise ValidationError(
                "Length of driver license must be 8 characters"
            )

        if not license_number_alpha.isupper():
            raise ValidationError("Check that you have 3 uppercase letter")
        elif not license_number_alpha.isalpha():
            raise ValidationError("Check that you have 3 uppercase letter")

        if not license_number_num.isnumeric():
            raise ValidationError("Check that you have five digits")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
