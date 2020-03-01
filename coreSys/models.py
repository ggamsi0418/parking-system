import uuid
from django.db import models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# Create your models here.
class Member(models.Model):
    member_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('NAME', max_length=15)
    phone = models.CharField(
        max_length=13, help_text='Contact phone number')
    member_car_number = models.CharField("MEMBER's CAR NUMBER", max_length=8)
    registration = models.DateField(auto_now=True)
    expiration = models.DateField(
        default=(datetime.now()+relativedelta(months=1)))

    def __str__(self):
        return self.name


class User(models.Model):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user_car_number = models.CharField("USER's CAR NUMBER", max_length=8)
    user_type = models.BooleanField(
        help_text="'0' is visitor, '1' is member")
    state = models.BooleanField(
        help_text="'0' is entry, '1' is exit")
    in_time = models.DateTimeField(auto_now_add=True)
    out_time = models.DateTimeField(null=True, blank=True)
    pee = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user_car_number
