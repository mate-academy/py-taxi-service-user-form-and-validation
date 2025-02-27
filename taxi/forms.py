from django import forms
from django.contrib.auth import get_user_model

from taxi.models import Car, validate_license


User = get_user_model()


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validate_license])

    class Meta:
        model = User
        fields = ["license_number"]
