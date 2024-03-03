from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django import forms
from django.forms import ModelForm

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r"\b[A-Z]{3}[0-9]{5}\b",
                message="Enter a valid license number",
                code="invalid_format"
            )
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreateForm(DriverLicenseUpdateForm, UserCreationForm):
    class Meta:
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "license_number",))


class CarForm(ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
