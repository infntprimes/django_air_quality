from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User

import datetime


def validate_date_in_range(date):
    if date < datetime.date(1970, 1, 1) or date >= datetime.date(2019, 1, 1):
        raise ValidationError(
            _('%(date) must be in the range [1970,2017]'),
            params={'date': date}
        )


def validate_zipcode(zipcode):
    if not str(zipcode).isnumeric() or len(str(zipcode)) is not 5:
        raise ValidationError(
            _('%(zipcode) must be exactly 5 numeric digits'),
            params={'zipcode': zipcode}
        )


class ZipcodeLatLong(models.Model):
    zipcode = models.CharField(max_length=5, validators=[validate_zipcode])
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    datetime_updated = models.DateTimeField()


class Report(models.Model):
    """
    Defines our model for a Report
    """
    zipcode = models.CharField(max_length=5, validators=[validate_zipcode])
    start_date = models.DateField(validators=[validate_date_in_range])
    end_date = models.DateField(validators=[validate_date_in_range])
    datetime_created = models.DateTimeField('Report Creation Date')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.zipcode + ": " + str(self.start_date) + "-" + str(self.end_date))

    def get_absolute_url(self):
        return reverse_lazy('airquality:index')
