from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car

LICENSE_NUMBER_REGEXP = "^[A-Z]{3}[0-9]{5}$"


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[RegexValidator(LICENSE_NUMBER_REGEXP)]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreateForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[RegexValidator(LICENSE_NUMBER_REGEXP)]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
