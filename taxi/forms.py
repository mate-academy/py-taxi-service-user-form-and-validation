from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name",
                                                 "username", "email")


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    LENGTH_OF_LICENSE = 8
    LETTERS_COUNT = 3
    NUMBERS_COUNT = 5

    license_number = forms.CharField(
        max_length=LENGTH_OF_LICENSE,
        required=True,
        validators=[
            RegexValidator(
                rf"^[A-Z]{{{LETTERS_COUNT}}}\d{{{NUMBERS_COUNT}}}$",
                (f"License number should contain {LETTERS_COUNT} big letters "
                 f"and {NUMBERS_COUNT} numbers")
            ),

        ]
    )


class CarCreateForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Car
        fields = "__all__"
