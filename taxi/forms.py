from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = str(self.cleaned_data["license_number"])
        if Driver.objects.filter(
                license_number=license_number).exclude(
                pk=self.instance.pk).exists():
            raise ValidationError("This license number is already in use.")
        if len(license_number) != 8:
            raise ValidationError("License number must be 8 characters.")

        prefix, suffix = license_number[:3], license_number[3:]

        if (not prefix.isalpha()
                or not prefix.isupper() or not suffix.isdigit()):
            raise ValidationError("License number have incorrect format.")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Car
        fields = "__all__"
