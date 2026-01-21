from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator


from taxi.models import Driver, Car


license_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="The license number must consist of 8 characters:"
            " the first 3 are capital letters, the last 5 are numbers."
)


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        max_length=8,
        validators=[license_validator]
    )
    cars = forms.ModelMultipleChoiceField(
        queryset=Car.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "email",
            "license_number",
            "cars",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        max_length=8,
        validators=[license_validator]
    )

    class Meta:
        model = Driver
        fields = ("license_number", )


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
