from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Driver, Car


def validate_license_number(value: str):
    if len(value) != 8:
        raise ValidationError(
            _("%(value)s is not 8 characters long"),
            params={"value": value}
        )
    if not value[:3].isupper() or not value[:3].isalpha():
        raise ValidationError(
            _("first 3 characters should be uppercase letters")
        )
    if not value[-5:].isnumeric():
        raise ValidationError(
            _("last 5 characters should be digits")
        )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[validate_license_number]
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[validate_license_number]
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
