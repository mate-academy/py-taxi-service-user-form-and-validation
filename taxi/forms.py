from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=255,
        label="License number",
        validators=[RegexValidator(r"^[A-Z]{3}\d{5}$"), ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
