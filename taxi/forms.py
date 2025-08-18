from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Car


class BaseDriverLicenseForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = str(self.cleaned_data["license_number"])
        qs = get_user_model().objects.all()
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.filter(license_number=license_number).exists():
            raise ValidationError("This license number is already in use.")
        if len(license_number) != 8:
            raise ValidationError("License number must be 8 characters.")
        prefix, suffix = license_number[:3], license_number[3:]
        if not prefix.isalpha() or not prefix.isupper() or not suffix.isdigit():
            raise ValidationError("License number has incorrect format.")
        return license_number


class DriverCreationForm(UserCreationForm, BaseDriverLicenseForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(BaseDriverLicenseForm):
    pass


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Car
        fields = "__all__"
