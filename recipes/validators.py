import pint
from pint.errors import UndefinedUnitError
from django.core.exceptions import ValidationError


def validate_unit_of_measure(value):
    units_reg = pint.UnitRegistry()
    try:
        units_reg[value]
    except UndefinedUnitError:
        raise ValidationError(f'{value} является не допустимой мерой счёта!')
    except:
        raise ValidationError('Неизвестное значение')
