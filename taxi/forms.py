from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from taxi.models import Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.LICENSE_NUMBER_LEN:
            raise ValidationError(
                f"Ensure that that length of license number is "
                f"{DriverLicenseUpdateForm.LICENSE_NUMBER_LEN}"
            )

        if (not license_number[
                :DriverLicenseUpdateForm.UPPERCASE_NUM].isupper()
                or not license_number[
                    :DriverLicenseUpdateForm.UPPERCASE_NUM].isalpha()):
            raise ValidationError(
                f"Ensure that first {DriverLicenseUpdateForm.UPPERCASE_NUM} "
                f"characters are uppercase letters"
            )

        if not license_number[
                DriverLicenseUpdateForm.UPPERCASE_NUM:].isdigit():
            raise ValidationError(
                f"Ensure that last {DriverLicenseUpdateForm.DIGIT_NUM} "
                f"characters are digits"
            )

        return license_number


class DriverLicenseUpdateForm(UserChangeForm):
    LICENSE_NUMBER_LEN = 8
    UPPERCASE_NUM = 3
    DIGIT_NUM = 5

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != DriverLicenseUpdateForm.LICENSE_NUMBER_LEN:
            raise ValidationError(
                f"Ensure that that length of license number is "
                f"{DriverLicenseUpdateForm.LICENSE_NUMBER_LEN}"
            )

        if (not license_number[
                :DriverLicenseUpdateForm.UPPERCASE_NUM].isupper()
                or not license_number[
                :DriverLicenseUpdateForm.UPPERCASE_NUM].isalpha()):
            raise ValidationError(
                f"Ensure that first {DriverLicenseUpdateForm.UPPERCASE_NUM} "
                f"characters are uppercase letters"
            )

        if not license_number[
                DriverLicenseUpdateForm.UPPERCASE_NUM:].isdigit():
            raise ValidationError(
                f"Ensure that last {DriverLicenseUpdateForm.DIGIT_NUM} "
                f"characters are digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
