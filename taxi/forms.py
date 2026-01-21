from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseMixin(forms.ModelForm):
    MAX_LENGTH = 8
    START = 3
    END = 5

    def clean_license_number(self) -> str | None:
        license_number = self.cleaned_data["license_number"]
        start = license_number[:self.START]
        end = license_number[-self.END:]
        if len(license_number) != self.MAX_LENGTH:
            raise ValidationError(
                f"License number must be equal {self.MAX_LENGTH} characters"
            )
        if not start.isalpha() or (start.isalpha() and not start.isupper()):
            raise ValidationError(
                f"First {self.START} characters must be upper letters"
            )
        if not end.isdigit():
            raise ValidationError(f"Last {self.END} characters must be digits")
        return license_number


class DriverLicenseUpdateForm(DriverLicenseMixin):

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverCreationForm(UserCreationForm, DriverLicenseMixin):

    class Meta(UserCreationForm.Meta):
        model = Driver
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


class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)
