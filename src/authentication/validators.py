from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_minimum_age(value):
    today = timezone.now().date()
    age = today.year - value.year - (
        (today.month, today.day) < (value.month, value.day)
        )
    if age < 15:
        raise ValidationError(
            'Vous devez avoir au minimum 15 ans pour vous inscrire.'
            )
