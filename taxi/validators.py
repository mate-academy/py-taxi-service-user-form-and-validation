from django.core.validators import RegexValidator

license_number_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="Numer musi składać się z 3 dużych liter i 5 cyfr.",
    code="invalid_license",
)
