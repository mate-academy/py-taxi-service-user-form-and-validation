from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Car


class DriverCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENCE_VALIDATOR = RegexValidator(regex=r"^[A-Z]{3}[0-9]{5}$")
    license_number = forms.CharField(
        required=True,
        validators=[LICENCE_VALIDATOR],
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number", )
        template_name = "taxi/driver_license_update.html"


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    LICENCE_VALIDATOR = RegexValidator(regex=r"^[A-Z]{3}[0-9]{5}$")
    license_number = forms.CharField(
        required=True,
        validators=[LICENCE_VALIDATOR],
    )

    class Meta:
        model = Car
        fields = "__all__"
