from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator

from taxi.models import Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    LICENSE_LENGTH = 8
    license_number = forms.CharField(
        required=True,
        validators=[
            MaxLengthValidator(LICENSE_LENGTH),
            MinLengthValidator(LICENSE_LENGTH)
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "license_number",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if (
                license_number[:3].isalpha()
                and license_number[:3].isupper()
                and license_number[-5:].isdigit()
        ):
            return license_number
        else:
            raise ValidationError(
                "Type correct license number."
            )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LENGTH = 8
    license_number = forms.CharField(
        required=True,
        validators=[
            MaxLengthValidator(LICENSE_LENGTH),
            MinLengthValidator(LICENSE_LENGTH)
        ]
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if (
                license_number[:3].isalpha()
                and license_number[:3].isupper()
                and license_number[-5:].isdigit()
        ):
            return license_number
        else:
            raise ValidationError(
                "Type correct license number."
            )
