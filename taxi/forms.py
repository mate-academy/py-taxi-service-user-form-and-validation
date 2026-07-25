from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import MinLengthValidator, RegexValidator, MaxLengthValidator

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(8),
            MaxLengthValidator(8),
            RegexValidator(regex=r"^[A-Z]{3}[0-9]{5}$")
        ]
    )
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", "email", "first_name", "last_name",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(8),
            RegexValidator(regex=r"^[A-Z]{3}[0-9]{5}$")
        ]
    )
    class Meta(UserChangeForm):
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Car
        fields = "__all__"


# class EmptyActionForm(forms.Form):
#     pass
