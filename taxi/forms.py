from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator, MaxValueValidator

from taxi.models import Car


class DriverRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class DriverLicenseUpdateForm(forms.Form):
    license_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="Valid license number consists of 3 uppercase letters"
                " and 5 digits",
            ),
        ],
        label=False,
    )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Car
        fields = "__all__"
