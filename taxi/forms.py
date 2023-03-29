from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import Driver, Car


class LicenseNumberField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(RegexValidator(
            regex=r"^[A-Z]{3}\d{5}$",
            message=("Please enter a valid driver\'s license number "
                     "consisting of 3 uppercase letters followed by 5 digits."
                     )
        ))


class DriverCreationForm(UserCreationForm):
    license_number = LicenseNumberField(max_length=8)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = LicenseNumberField(max_length=8)

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
