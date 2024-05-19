from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

# Create your models here


class Guest(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    mobile = mobile = models.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                # ensures that the mobile number either starts with "+88" followed by "0" and then 10 digits or starts with "0" followed by 10 digits.
                regex=r"^\+880?\d{10}$|^0\d{10}$",
                message="Enter a valid Bangladeshi mobile number.",
            )
        ],
    )
    address = models.CharField(max_length=255)
