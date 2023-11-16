from django.core.validators import RegexValidator

license_number_validator = [RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="License_number should consist only of 8 characters: "
            "first 3 characters are uppercase letters, "
            "last 5 characters are digits"
)]
