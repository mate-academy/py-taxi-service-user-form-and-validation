from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator

from taxi.models import Car


class LicenseMixin(forms.ModelForm):
    LETTERS = 3
    NUMBERS = 5
    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                fr"^[A-Z]{{{LETTERS}}}[0-9]{{{NUMBERS}}}$",
                message=f"License number must consist "
                        f"first {LETTERS} uppercase letters and "
                        f"last {NUMBERS} digits"
            )
        ]
    )


class DriverForm(LicenseMixin, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdate(LicenseMixin, forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ("license_number", )


class CarForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
