from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model


from .models import Driver, Car


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(max_length=8)

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)
        widgets = {
            "license_number": forms.TextInput(
                attrs={
                    "placeholder": "XXX00000",
                    "maxlength": "8",
                })
        }


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("drivers",)
