# taxi/forms.py
import re
from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
# Sugestão: Se User não for usado no forms, remova a importação.
# from .models import Driver, Car, User
from .models import Driver, Car # Removido User, como sugerido

# --- Validação Customizada da CNH ---
def validate_license_format(value):
    """
    Valida se a licença:
    1. Tem exatamente 8 caracteres.
    2. Os 3 primeiros são letras maiúsculas.
    3. Os 5 últimos são dígitos.
    """
    if not re.fullmatch(r"[A-Z]{3}\d{5}", value):  # Corrigido E262
        raise ValidationError(
            "A licença deve ter 8 caracteres: 3 letras maiúsculas seguidas por 5 dígitos"  # Corrigido E501
            " (ex: ABC12345)."  # Corrigido E501
        )


# E302: Duas linhas em branco após a função

# --- Formulário para Criação/Atualização de Driver (Inclui validação) ---
class DriverForm(forms.ModelForm):
    # Mantido como 'license' para mapear corretamente para o modelo Driver.license
    license = forms.CharField(
        max_length=8,
        validators=[validate_license_format],
        label="Número da CNH"
    )

    class Meta:
        model = Driver
        fields = ["first_name", "last_name", "license", "bio"]  # Corrigido E501

    def clean_license(self):
        # A validação já está no field, mas mantemos a chamada explícita como prática
        license_val = self.cleaned_data.get("license")
        validate_license_format(license_val)  # Chamada para garantir
        return license_val


# E302: Duas linhas em branco após a classe

# --- Formulário Específico para Atualização da CNH ---
class DriverLicenseUpdateForm(forms.Form):
    license = forms.CharField(
        max_length=8,
        validators=[validate_license_format],
        label="Novo Número da CNH"
    )

    def clean_license(self):
        license_val = self.cleaned_data["license"]
        validate_license_format(license_val)  # Chamada para garantir
        return license_val


# E302: Duas linhas em branco após a classe

# --- Formulário para Criação de Carro (com Checkboxes para Drivers) ---
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "plate_number", "drivers"]

        widgets = {
            # Switch para checkboxes
            "drivers": widgets.CheckboxSelectMultiple,
        }
