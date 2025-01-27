from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    ReadOnlyPasswordHashField
)

from taxi.models import Driver, Car


class LicenseNumberField(forms.CharField):
    def __init__(self, *args, **kwargs):
        default_kwargs = {
            "required": True,
            "max_length": 8,
            "help_text": _(
                "Required. "
                "8 characters. "
                "Three capital letters A-Z, followed by 5 digits"
            ),
            "validators": [
                RegexValidator(
                    regex=r"[A-Z]{3}[0-9]{5}",
                    message=_(
                        "Invalid license number. "
                        "Must be three capital letters (A-Z), "
                        "followed by 5 digits"
                    )
                ),
            ],
            "error_messages": {
                "unique": _("Driver with this license number already exists"),
            }
        }
        kwargs.update(default_kwargs)
        super().__init__(*args, **kwargs)


class DriverCreationForm(UserCreationForm):
    license_number = LicenseNumberField()

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(UserChangeForm):
    license_number = LicenseNumberField()

    password = ReadOnlyPasswordHashField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Driver
        fields = ["license_number", ]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(
                attrs={"class": "form-select drivers-field", "size": "5"}
            )
        }
