from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ('license_number',)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if not license_number[:3].isupper():
            raise ValidationError("Ensure that value starts with  3 uppercase letters")
        if not license_number[-5:].isdigit():
            raise ValidationError("Ensure that value ends with 5 digits")
        if not len(license_number) == 8:
            raise ValidationError("Ensure that length of your licence exactly 8 characters")


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
