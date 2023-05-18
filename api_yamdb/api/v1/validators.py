import datetime
import re

from django.core.exceptions import ValidationError


def me_forbidden(value):
    if value == 'me':
        raise ValidationError('Запрещенный никнейм!')
    return value


def year_validation(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            (f'Ошибка! Значение года не может быть равно {value}!')
        )


def username_symbols(value):
    for char in value:
        if not re.search(r'^[\w@.+-_]+$', char):
            raise ValidationError(f'Недопустимый символ: "{char}"!')
