from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_data = self.cleaned_data["license_number"]
        if len(license_data) != 8:
            raise ValidationError("Number of characters must be 8")
        part_1 = license_data[:3]
        part_2 = license_data[3:]
        if not part_1.isalpha():
            raise ValidationError("First characters must be letters")
        if not part_1.isupper():
            raise ValidationError("First characters must be capital letters")
        if not part_2.isdecimal():
            raise ValidationError("Last 5 characters must be digits")
        return license_data


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"
