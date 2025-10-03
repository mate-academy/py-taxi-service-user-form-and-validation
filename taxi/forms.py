from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django import forms

from .models import Driver


class DriverCreationForm(UserCreationForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name",)


class DriverLicenseForm(forms.ModelForm):

    license_number = forms.CharField(
        max_length=8,
        min_length=8,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{3}[0-9]{5}$',
            )
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)
