from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Driver, Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple()
        }


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number", )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if len(license_number) != 8:
            raise forms.ValidationError(
                "Номер должен состоять из 8 символов."
            )

        first_part = license_number[:3]
        second_part = license_number[3:]

        if not first_part.isalpha() or not first_part.isupper():
            raise forms.ValidationError(
                "Первые три символа должны быть заглавным буквами."
            )
        if not second_part.isdigit():
            raise forms.ValidationError(
                "Последние 5 символов должны быть цифрами."
            )

        return license_number
