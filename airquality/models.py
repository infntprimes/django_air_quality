from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User

import datetime


def validate_start_date(end_date):
    if end_date < datetime.date(1970, 1, 1):
        raise ValidationError(
            _('%(start_date) must be before ' + str(end_date)),
            params={'start_date': end_date}
        )


def validate_end_date(end_date):
    current_year = datetime.datetime.now().year
    if end_date >= datetime.date(current_year, 1, 1):
        raise ValidationError(
            _('%(end_date) must be before ' + str(current_year)),
            params={'end_date': end_date}
        )


def validate_zipcode(zipcode):
    if not str(zipcode).isnumeric() or len(str(zipcode)) is not 5:
        raise ValidationError(
            _('%(zipcode) must be exactly 5 numeric digits'),
            params={'zipcode': zipcode}
        )


class Report(models.Model):
    zipcode = models.CharField(max_length=5, validators=[validate_zipcode])
    start_date = models.DateField(validators=[validate_start_date])
    end_date = models.DateField(validators=[validate_end_date])
    datetime_created = models.DateTimeField('Report Creation Date')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.zipcode + ": " + str(self.start_date) + "-" + str(self.end_date))

    def get_absolute_url(self):
        return reverse_lazy('airquality:index')


