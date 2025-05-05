from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class LicenseNumberFieldMixin(forms.Form):
    license_number = forms.CharField(
        max_length=8,
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message="License number must start with 3 uppercase letters "
                        "followed by 5 digits. Example: ABC12345"
            )
        ]
    )


class DriverCreationForm(UserCreationForm, LicenseNumberFieldMixin):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=70, required=False)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number", "email"
        )


class DriverLicenseUpdateForm(LicenseNumberFieldMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
