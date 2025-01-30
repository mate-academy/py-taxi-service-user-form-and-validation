from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


Driver = get_user_model()


def validate_license_number(value) -> None:
    if not value.isalnum() or len(value) != 8:
        raise ValidationError("License must consist of 8 characters.")
    if not value[:3].isalpha() or not value[:3].isupper():
        raise ValidationError(
            "The first 3 characters must be uppercase letters."
        )
    if not value[3:].isdigit():
        raise ValidationError("The last 5 characters must be digits.")


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def save(self, commit=True):
        user = super().save(commit=False)
        validate_license_number(self.cleaned_data["license_number"])
        if commit:
            user.save()
        return user


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(validators=[validate_license_number])

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
