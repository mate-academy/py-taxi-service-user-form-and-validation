from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from taxi.models import Car
from django import forms


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        value = self.cleaned_data["license_number"].strip().upper()
        if len(value) != 8:
            raise ValidationError("License must be 8 characters")
        if not value[:3].isalpha():
            raise ValidationError("First 3 characters must be letters")
        if not value[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits")
        return value


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["license_number"]

    def clean_license_number(self):
        value = self.cleaned_data["license_number"].strip().upper()
        if len(value) != 8:
            raise ValidationError("License must be 8 characters")
        if not value[:3].isalpha():
            raise ValidationError("First 3 characters must be letters")
        if not value[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits")
        return value


class CarForm(ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Car
        fields = "__all__"
