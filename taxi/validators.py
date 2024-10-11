from django import forms
from django.core.validators import MaxLengthValidator, RegexValidator


LICENSE_NUMBER_VALIDATION = forms.CharField(
    required=True,
    validators=[
        MaxLengthValidator(8),
        RegexValidator(
            regex=r"^[A-Z]{3}\d{5}$",
            message="License number must be in the format 'AAA12345'."
        ),
    ],
)
