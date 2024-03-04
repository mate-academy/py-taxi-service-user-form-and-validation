from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_num = str(self.cleaned_data["license_number"])

        if len(license_num) != 8:
            raise ValidationError(
                "The license number provided does not have 8 characters"
            )

        if not license_num[:3].isalpha() or not license_num[:3].isupper():
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )

        if not license_num[-5:].isdigit():
            raise ValidationError(
                "Last 5 characters must be digits"
            )

        return license_num


class OriginCarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
