from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car
from django import forms


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"

    def clean_password(self):
        password = self.cleaned_data["password"]

        if len(password) != 8:
            raise ValidationError("Length of password must be 8 elemenets")
        if password[:3] != password[:3].upper():
            raise ValidationError("First 3 elements must be in upper case")
        if not password[3:].isdigit():
            raise ValidationError("Last 5 elements must be digits")

        return password


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Driver
        fields = "__all__"
