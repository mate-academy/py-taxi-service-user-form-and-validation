from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        number = self.cleaned_data["license_number"]
        if len(number) != 8:
            raise ValidationError("Password must be 8 length")
        if not number[:3].isalpha():
            raise ValidationError("Word must be A-Z")
        if number[:3] != number[:3].upper():
            raise ValidationError("Number must be upper")
        if not number[3:].isnumeric():
            raise ValidationError("Must be 5 last numeric symbol")
        return number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        number = self.cleaned_data["license_number"]
        if len(number) != 8:
            raise ValidationError("Password must be 8 length")
        if not number[:3].isalpha():
            raise ValidationError("Word must be A-Z")
        if number[:3] != number[:3].upper():
            raise ValidationError("Number must be upper")
        if not number[3:].isnumeric():
            raise ValidationError("Must be 5 last numeric symbol")
        return number


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"
