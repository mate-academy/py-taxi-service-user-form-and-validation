from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message=""
                        "The license number should consist of "
                        "3 uppercase letters "
                        "followed by 5 digits."
            )
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreate(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
