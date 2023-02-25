from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            f'{value} введите корректно год'
        )


def validate_genry_null(value):
    if value is None:
        raise ValidationError(
            f'{value} Поле пустое'
        )
