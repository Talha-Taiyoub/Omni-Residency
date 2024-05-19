from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
# source C:/Users/ASUS/.virtualenvs/Omni-Residency-N85yyym9/Scripts/activate


class Destination(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


# branch logo is an image and branch manager will be a user_id,later both will be added
class Branch(models.Model):
    name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255, null=True, blank=True)
    destination = models.ForeignKey("Destination", on_delete=models.PROTECT)
    branch_initial = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r"^[A-Z0-9]{1,7}$",
                message="Initials must be 1-7 characters long and contain only uppercase letters and numbers.",
            )
        ],
    )
    branch_address = models.CharField(max_length=255)
    overview = models.TextField()
    email = models.EmailField(unique=True)
    telephone = models.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                # ensures that the phone number starts with either a plus sign or a digit, and the rest of the characters are digits
                regex=r"^[+\d][\d]+$",
                message="Enter a valid telephone number.",
            )
        ],
    )
    mobile = models.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                # ensures that the mobile number either starts with "+88" followed by "0" and then 10 digits or starts with "0" followed by 10 digits.
                regex=r"^\+880?\d{10}$|^0\d{10}$",
                message="Enter a valid Bangladeshi mobile number.",
            )
        ],
    )
    location_iframe = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
