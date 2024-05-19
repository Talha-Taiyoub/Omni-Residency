from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from community.models import Guest

# Create your models here.
# source C:/Users/ASUS/.virtualenvs/Omni-Residency-N85yyym9/Scripts/activate


class Destination(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# branch logo is an image and branch manager will be a user_id,later both will be added
class Branch(models.Model):
    name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255, null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.PROTECT)
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


ACTIVE = "A"
OUT_OF_ORDER = "O"
ROOM_STATUS = [(ACTIVE, "Active"), (OUT_OF_ORDER, "Out of order")]


# Featured Image, gallery, amenities, panorama will be added later
class RoomCategory(models.Model):
    room_name = models.CharField(max_length=50)
    status = models.CharField(max_length=1, choices=ROOM_STATUS, default=OUT_OF_ORDER)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    overview = models.TextField()
    adults = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    children = models.PositiveSmallIntegerField()
    regular_price = models.DecimalField(max_digits=9, decimal_places=2)
    discount_price = models.DecimalField(max_digits=9, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Room(models.Model):
    room_number = models.CharField(max_length=5)
    room_category = models.ForeignKey(RoomCategory, on_delete=models.PROTECT)
    status = models.CharField(max_length=1, choices=ROOM_STATUS, default=OUT_OF_ORDER)


PENDING = "PN"
CONFIRMED = "CN"
CHECKED_OUT = "CO"
BOOKING_STATUS = [
    (PENDING, "Pending"),
    (CONFIRMED, "Confirmed"),
    (CHECKED_OUT, "Checked_out"),
]


class Booking(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
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

    guest_id = models.ForeignKey(
        Guest, on_delete=models.SET_NULL, null=True, blank=True
    )
    room_type = models.ForeignKey(RoomCategory, on_delete=models.PROTECT)
    assigned_room = models.ForeignKey(Room, on_delete=models.PROTECT)
    status = models.CharField(max_length=2, choices=BOOKING_STATUS, default=PENDING)
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    children = models.PositiveSmallIntegerField()

    def clean(self):
        super().clean()
        if self.check_out <= self.check_in:
            raise ValidationError(
                {"check_out": _("Check-out date must be later than check-in date.")}
            )


class Billing(models.Model):
    pass
