from .models import Car
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = (
        forms.CharField(
            max_length=8,
            min_length=8,
            validators=[
                RegexValidator(
                    regex=r"^[A-Z]{3}\d{5}$",
                    message="Format: AAA12345"
                )
            ]
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class DriverCreationForm(UserCreationForm):
    license_number = (
        forms.CharField(
            max_length=8,
            min_length=8,
            validators=[
                RegexValidator(
                    regex=r"^[A-Z]{3}\d{5}$",
                    message="Format: AAA12345"
                )
            ]
        )
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
