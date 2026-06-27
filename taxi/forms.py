from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}[0-9]{5}$",
                message="License must consist 8 characters: "
                        "3 uppercase letters, 5 numbers.",
                code="invalid_license_format",
            )
        ],
    )

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
            "email",
            "password1",
            "password2",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}[0-9]{5}$",
                message="License must consist 8 characters: "
                        "3 uppercase letters, 5 numbers.",
                code="invalid_license_format",
            )
        ],
        widget=forms.TextInput(
            attrs={"placeholder": "XYZ12345"}
        ),
    )

    class Meta:
        model = get_user_model()
        fields = [
            "license_number",
        ]
