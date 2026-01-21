from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Car


class DriverCreationForm(UserCreationForm):

    license_number = forms.CharField(
        required=True,
        validators=[RegexValidator(regex=r"^[A-Z]{3}\d{5}$",
                                   message="Invalid license number")],
    )

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number", )


class DriverLicenseUpdateForm(forms.ModelForm):

    license_number = forms.CharField(
        required=True,
        validators=[RegexValidator(regex=r"^[A-Z]{3}\d{5}$",
                                   message="Invalid license number")],
    )

    class Meta:
        model = get_user_model()
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Car
        fields = "__all__"


class CarUpdateForm(forms.ModelForm):

    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Car
        fields = "__all__"
