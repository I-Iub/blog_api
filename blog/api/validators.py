from rest_framework.serializers import ValidationError

def check_natural_number(value, name):
    try:
        number = int(value)
        if number < 1:
            raise ValidationError(
                {f"{name}": "Число должно быть больше нуля"}
            )
    except ValueError:
        raise ValidationError(
            {f"{name}": "Число должно быть натуральным"}
        )
    return number
