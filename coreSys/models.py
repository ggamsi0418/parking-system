from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from django.db import models
from django import forms
import uuid
import re


# Create your models here.
class Member(models.Model):
    '''
    정기 회원 테이블
    '''
    member_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('NAME', max_length=15)
    phone = models.CharField(
        max_length=13, help_text='Contact phone number')
    member_car_number = models.CharField(
        "MEMBER's CAR NUMBER", max_length=8)
    registration = models.DateField(auto_now=True)
    expiration = models.DateField(
        default=(datetime.now()+relativedelta(months=1)))

    def __str__(self):
        return self.name


class User(models.Model):
    '''
    주차장 이용객 테이블
    '''
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user_car_number = models.CharField("USER's CAR NUMBER", max_length=8)
    user_type = models.NullBooleanField(
        help_text="'0' is visitor, '1' is member")
    state = models.BooleanField(
        default=False, help_text="'0' is entry, '1' is exit")
    in_time = models.DateTimeField(auto_now_add=True)
    out_time = models.DateTimeField(null=True, blank=True)
    fee = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user_car_number
