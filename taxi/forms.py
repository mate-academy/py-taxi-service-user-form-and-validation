from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car
from taxi.validators import license_number_validator


class DriverUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=256, required=True)
    last_name = forms.CharField(max_length=256, required=True)
    license_number = forms.CharField(
        required=True,
        validators=license_number_validator
    )

    class Meta(UserCreationForm.Meta):
        FIELDS = ("first_name", "last_name", "license_number")
        model = Driver
        fields = UserCreationForm.Meta.fields + FIELDS


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class CarDriverAssignForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm, ):
    license_number = forms.CharField(validators=license_number_validator)

    class Meta:
        model = Driver
        fields = ("license_number",)
