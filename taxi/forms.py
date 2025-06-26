from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.middleware import get_user
from django.core.validators import MinLengthValidator, MaxLengthValidator

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    length = 8
    license_number = forms.CharField(
        required=True,
        validators=[MinLengthValidator(length),
                    MaxLengthValidator(length)]
    )

    class Meta:
        model = Driver
        fields = ["license_number", ]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if not license_number[:3].isupper():
            raise forms.ValidationError("First three symbols "
                                        "must be uppercase letters")
        elif not license_number[4:].isdigit():
            raise forms.ValidationError("Last five symbols must be digits")
        return license_number


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
