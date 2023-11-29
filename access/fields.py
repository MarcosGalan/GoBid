from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError, CharField

from access.utils import is_valid_id


class DNIField(CharField):
    default_error_messages = {
        'invalid': 'Please, enter a valid DNI',
    }

    def clean(self, value):
        super(CharField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''

        first_letter = value[0]
        type_id = "nif"
        try:
            int(first_letter)
        except ValueError:
            type_id = "nie"

        if is_valid_id(type_id, value):
            return value

        raise ValidationError(self.error_messages['invalid'])
