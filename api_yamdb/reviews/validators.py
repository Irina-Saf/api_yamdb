from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value > timezone.now().year or value < 0:
        raise ValidationError(
            f'{value} введите корректно год'
        )


def validate_genry_null(value):
    # if value is None:
    print(f'!!!!!!!!!!!!!!!!!!!!!{value}')
    if not value:
        raise ValidationError(
            f'{value} Поле пустое'
        )
