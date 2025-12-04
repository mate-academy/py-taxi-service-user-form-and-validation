from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = get_user_model()
        fields = ("license_number",)


class CarCreationForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(forms.ModelForm):
        model = Car
        fields = "__all__"
