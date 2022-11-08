from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.forms import CheckboxSelectMultiple

from taxi.models import Car


class LicenseValidatorMixin(forms.ModelForm):
    NUMBERS = 5
    LETTERS = 3
    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                rf"^[A-Z]{{{LETTERS}}}[0-9]{{{NUMBERS}}}$",
                message="The license must consist"
                        f"first {NUMBERS} characters are uppercase letters and"
                        f"last {LETTERS} characters are digits"
            )
        ]
    )


class DriverCreateForm(LicenseValidatorMixin, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number", "first_name", "last_name")


class DriverLicenseUpdateForm(LicenseValidatorMixin, forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
