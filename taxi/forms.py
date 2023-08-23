from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django import forms
from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    NORMAL_LENGTH_VALUE = 8

    license_number = forms.CharField(
        required=True,
        validators=[
            MaxLengthValidator(NORMAL_LENGTH_VALUE),
            MinLengthValidator(NORMAL_LENGTH_VALUE),
        ],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not (license_number[:3].isupper() and license_number[:3].isalpha()):
            raise ValidationError(
                "First three characters must be capital letters"
            )

        if not license_number[3:].isdigit():
            raise ValidationError(
                "Last 5 characters must be digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
