from django.db import models

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
