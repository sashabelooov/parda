from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

def validate_uz_phone(value):
    if not value.startswith('+998'):
        raise ValidationError('Phone must start with +998')
    if len(value) != 13:
        raise ValidationError('Phone must be 13 characters long')
    if not value[4:].isdigit():
        raise ValidationError('Phone must contain only digits after +998')
    code = value[4:6]
    allowed_codes = ['93', '94', '55', '97', '88', '90', '91', '98', '95', '99', '77', '33']
    if code not in allowed_codes:
        raise ValidationError(f'Invalid code {code}. Allowed: {", ".join(allowed_codes)}')

class CustomUser(AbstractUser):
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[validate_uz_phone]
    )
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.phone
        self.full_clean()
        super().save(*args, **kwargs)