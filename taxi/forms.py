from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import MaxLengthValidator, RegexValidator
from django.forms import models

from taxi.models import Driver, Car


class DriverLicenceMixin(forms.Form):
    license_number = forms.CharField(
        validators=[
            MaxLengthValidator(8),
            RegexValidator(
                regex=r"^[A-Z]{3}[0-9]{5}$",
                message="Please enter a valid license number "
                        "(3 capital letters and 5 numbers)."
            )
        ]
    )


class DriverCreationForm(DriverLicenceMixin, UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(DriverLicenceMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = models.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
