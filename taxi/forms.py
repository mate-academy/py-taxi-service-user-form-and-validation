from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from taxi.models import Driver, Car


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        label="characters license_number",
        widget=forms.TextInput(attrs={
            "placeholder": "Entry 8 characters of license"}),
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", )
        labels = {"license_number": "Characters license_number", }

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise ValidationError("License must be 8 characters.")

        first_3 = license_number[:3]
        last_5 = license_number[-5:]

        if not first_3.isupper() or not first_3.isalpha():
            raise ValidationError(
                "First 3 characters must be uppercase letters."
            )

        if not last_5.isdigit():
            raise ValidationError("Last 5 characters must be digits.")

        current_driver_id = self.instance.pk if self.instance else None
        if (Driver.objects.filter(license_number=license_number)
                .exclude(pk=current_driver_id).exists()):
            raise ValidationError("This license already exists.")
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)
        labels = {"license_number": "Characters license_number", }

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise ValidationError("License must be 8 characters.")

        first_3 = license_number[:3]
        last_5 = license_number[-5:]

        if not first_3.isupper() or not first_3.isalpha():
            raise ValidationError("First 3 characters must be uppercase"
                                  " letters.")

        if not last_5.isdigit():
            raise ValidationError("Last 5 characters must be digits.")

        current_driver_id = self.instance.pk if self.instance else None
        if (Driver.objects.filter(license_number=license_number)
                .exclude(pk=current_driver_id).exists()):
            raise ValidationError("This license already exists.")

        return license_number
