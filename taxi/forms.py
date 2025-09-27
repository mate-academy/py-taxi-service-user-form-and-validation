from __future__ import annotations

import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Driver, Car

# 3 letras maiúsculas + 5 dígitos, total 8
_LICENSE_RE = re.compile(r"^[A-Z]{3}\d{5}$")


def _validate_license(value: str) -> str:
    """Normaliza para maiúsculas e valida o padrão do license_number."""
    value = (value or "").upper()
    if not _LICENSE_RE.fullmatch(value):
        raise ValidationError(
            "License number must be 8 chars: 3 uppercase letters + 5 digits."
        )
    return value


class DriverCreationForm(UserCreationForm):
    """Form de criação de Driver com validação do license_number."""

    class Meta(UserCreationForm.Meta):
        model = Driver
        # UserCreationForm já inclui username, password1 e password2
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self) -> str:
        return _validate_license(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    """Atualiza apenas o license_number, com a mesma validação."""

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        return _validate_license(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    """Mostra drivers (M2M) como checkboxes no formulário do Car."""
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
