from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


def validate_license_number(number, instance=None):
    if len(number) != 8:
        raise forms.ValidationError("License number must be 8 characters.")
    letters, digits = number[:3], number[3:]
    if not letters.isupper() or not letters.isalpha():
        raise forms.ValidationError(
            "First 3 characters must be uppercase letters."
        )
    if not digits.isdigit():
        raise forms.ValidationError("Last 5 characters must be digits.")
    qs = get_user_model().objects.filter(license_number=number)
    if instance:
        qs = qs.exclude(pk=instance.pk)
    if qs.exists():
        raise forms.ValidationError("This license number is already in use.")


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(max_length=8, required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        number = self.cleaned_data["license_number"]
        validate_license_number(number, instance=None)
        return number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        number = self.cleaned_data["license_number"]
        validate_license_number(number, instance=self.instance)
        return number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers")
