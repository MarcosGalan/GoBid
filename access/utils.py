from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError


def fiscal_letter(fiscal_num=None):
    """return the correct letter for the fiscal_num param"""
    if fiscal_num:
        result = fiscal_num % 23
        letters = 'TRWAGMYFPDXBNJZSQVHLCKE'
        return letters[result]
    return fiscal_num


def is_valid_id(dni_type, number):
    """"""
    is_valid = False
    if dni_type == 'nif':
        if number[0:8].isdigit() and len(number) == 9:
            letter = fiscal_letter(int(number[0:8]))
            is_valid = number[8].upper() == letter

    elif dni_type == 'nie':
        correct_length = len(number) == 10 or len(number) == 9
        correct_letter = number[0].upper() == 'X' or number[0].upper() == 'Y'
        correct_digits = number[1:len(number) - 1].isdigit()

        if correct_digits and correct_length and correct_letter:
            letter = fiscal_letter(int(number[1:-1]))
            is_valid = number[-1].upper() == letter
    else:
        is_valid = True

    return is_valid

