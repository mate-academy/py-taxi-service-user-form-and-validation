from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class ValidationMixin:

    @staticmethod
    def check_license_number(
            license_number: str
    ) -> None:
        if len(license_number) != 8:
            raise ValidationError("License number must contain 8 chars")

        for i, char in enumerate(license_number):
            if i < 3:
                if not char.isalpha() or not char.isupper():
                    raise ValidationError(
                        "First three chars, must be an uppercase letters!"
                    )
            else:
                if not char.isdigit():
                    raise ValidationError(
                        "Last five chars, must be an digits!"
                    )


class DriverCreateForm(ValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
            "email",
        )

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        self.check_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(ValidationMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        self.check_license_number(license_number)
        return license_number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
