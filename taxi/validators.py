from django.core.validators import RegexValidator

code_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="Must be 3 uppercase letters followed by 5 digits",
)
