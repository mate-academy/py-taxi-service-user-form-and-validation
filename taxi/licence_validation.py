from django.core.exceptions import ValidationError


def contains_only_digits(input_string):
    for char in input_string:
        if not char.isdigit():
            return True
    return False


def contains_only_letters(input_string):
    for char in input_string:
        if not char.isalpha():
            return True
    return False


def licence_number_validation(input_number):

    letters_part = input_number[:3]
    digits_part = input_number[3:]

    if len(input_number) != 8:
        raise ValidationError(
            "Ensure that license_number consist of 8 characters"
        )

    if contains_only_letters(letters_part):
        raise ValidationError(
            "Ensure that first 3 characters consist of letters"
        )

    if not letters_part.isupper():
        raise ValidationError(
            "Ensure that characters in uppercase"
        )

    if contains_only_digits(digits_part):
        raise ValidationError(
            "Ensure that last 5 characters consist of digits"
        )
    return input_number
