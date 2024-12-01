from django import forms
from .models import Driver, Car
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise (forms.ValidationError
                   ("License number must be exactly 8 characters."))
        if (not license_number[:3].isupper()
                or not license_number[:3].isalpha()):
            raise (forms.ValidationError
                   ("The first 3 characters must be uppercase letters."))
        if not license_number[3:].isdigit():
            raise (forms.ValidationError
                   ("The last 5 characters must be digits."))
        return license_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Update"))


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "drivers": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))
