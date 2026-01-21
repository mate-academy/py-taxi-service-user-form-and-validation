from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                "License number must be exactly 8 characters long."
            )
        first_part = license_number[:3]
        second_part = license_number[3:]
        if first_part != first_part.upper() or not first_part.isalpha():
            raise ValidationError(
                "The first three characters must be uppercase letters."
            )
        if not second_part.isdigit():
            raise ValidationError("The last five characters must be digits.")

        return license_number


class DriverLicenseUpdateForm(DriverForm):
    class Meta(DriverForm.Meta):
        fields = ("license_number",)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields.pop("password1", None)
        self.fields.pop("password2", None)

    def save(self, commit=True) -> Driver:
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
