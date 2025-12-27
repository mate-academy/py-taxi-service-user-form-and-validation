from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        min_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="License must have 3 uppercase "
                        "letters followed by 5 digits.",
                code="invalid_license_number"
            )
        ])

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreationForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )
