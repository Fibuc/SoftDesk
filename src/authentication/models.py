from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from .validators import validate_minimum_age


class User(AbstractUser):
    birth_date = models.DateField(validators=[validate_minimum_age])
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username
    
    def is_account_owner(self, user):
        return self == user