from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from community.models import Guest
from segment.models import Branch

# Create your models here.


class Cuisine(models.Model):
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)


ACTIVE = "A"
OUT_OF_ORDER = "O"
RESTAURANT_STATUS = [(ACTIVE, "Active"), (OUT_OF_ORDER, "Out of order")]


# Featured Image,Gallery will be added later
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    status = models.CharField(max_length=1, choices=RESTAURANT_STATUS, default=ACTIVE)
    overview = models.TextField()
    cuisine = models.ManyToManyField(Cuisine)
    breakfast_opening = models.TimeField()
    breakfast_closing = models.TimeField()
    lunch_opening = models.TimeField()
    lunch_closing = models.TimeField()
    dinner_opening = models.TimeField()
    dinner_closing = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)


PENDING = "PEN"
CONFIRMED = "CON"
COMPLETED = "COM"
CANCELLED = "CAN"
RESERVATION_CHOICES = [
    (PENDING, "Pending"),
    (CONFIRMED, "Confirmed"),
    (COMPLETED, "Completed"),
    (CANCELLED, "Cancelled"),
]


class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=3, choices=RESERVATION_CHOICES, default=PENDING
    )
    guest_name = models.CharField(max_length=50)
    guest_email = models.EmailField()
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
    number_of_people = models.IntegerField(validators=[MinValueValidator(1)])
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    # in admin we will use this field against reservation description
    additional_info = models.TextField(null=True, blank=True)
    total_bill = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )


ACTIVE = "A"
OUT_OF_ORDER = "O"
GYM_STATUS = [(ACTIVE, "Active"), (OUT_OF_ORDER, "Out of order")]

MALE = "M"
FEMALE = "F"
GENDER_CHOICES = [(MALE, "Male"), (FEMALE, "Female")]


class Gender(models.Model):
    name = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


# Featured image, gallery will be added later
class Gym(models.Model):
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    status = models.CharField(max_length=1, choices=GYM_STATUS, default=ACTIVE)
    overview = models.TextField()
    area = models.PositiveSmallIntegerField(default=0)
    fees = models.DecimalField(max_digits=9, decimal_places=2)
    opening = models.TimeField()
    closing = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class GymGender(models.Model):
    gender = models.ForeignKey(
        Gender, on_delete=models.PROTECT, related_name="gender_allowance"
    )
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


PENDING = "P"
APPROVED = "A"
DECLINED = "D"
GYM_MEMBERSHIP_CHOICES = [
    (PENDING, "Pending"),
    (APPROVED, "Approved"),
    (DECLINED, "Declined"),
]


class Membership(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
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
    # Why am I keeping fees? Because the manager of the gym may provide discounts for some particular guests
    fees = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.CharField(
        max_length=1, choices=GYM_MEMBERSHIP_CHOICES, default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
