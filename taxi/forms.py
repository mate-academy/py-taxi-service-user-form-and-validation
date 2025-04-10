from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(forms.ModelForm):
    LEN_OF_LICENSE_NUMBER = 8
    license_number = forms.CharField(
        required=True,
        max_length=LEN_OF_LICENSE_NUMBER,
        min_length=LEN_OF_LICENSE_NUMBER
    )

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if (not license_number[:3].isalpha()
                or not license_number[:3].isupper()):
            raise ValidationError(
                "Ensure the first 3 characters are uppercase letters"
            )
        elif not license_number[3:].isdigit():
            raise ValidationError("Ensure the last 5 characters are digits")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
