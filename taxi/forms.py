from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from taxi.models import Driver, Car


class DriverUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    @staticmethod
    def validate_uppercase_first_three(value):
        if not (value[:3].isalpha() and value[:3] == value[:3].upper()):
            raise ValidationError(
                "Invalid value: "
                "not capitalized first 3 characters (must be only letters)",
                code="invalid",
                params={"value": value}
            )

    @staticmethod
    def validate_last_five_digits(value):
        if value[3:].isdigit() is False:
            raise ValidationError(
                "Invalid value: must be only digits last 5 characters",
                code="invalid",
                params={"value": value}
            )

    license_number = forms.CharField(
        required=True,
        validators=[
            MaxLengthValidator(8),
            MinLengthValidator(8),
            validate_uppercase_first_three,
            validate_last_five_digits,
        ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
