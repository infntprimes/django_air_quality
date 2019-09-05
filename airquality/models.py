from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User

import datetime


def validate_date_in_range(date):
    if date < datetime.date(1970, 1, 1) or date >= datetime.date(2018, 1, 1):
        raise ValidationError(
            "date {0} must be in the range [1970,2017]".format(date)
        )


def validate_zipcode(zipcode):
    if not str(zipcode).isnumeric() or len(str(zipcode)) is not 5:
        raise ValidationError("zipcode must be 5 numeric digits")




class Report(models.Model):
    """
    Defines our model for a user-submitted Report request
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

class AirQualityReport(models.Model):
    """
    Defines our model for a completed air quality report
    """
    #userRequest = models.ForeignKey(Report, on_delete=models.CASCADE)
    AQI_green_days = models.IntegerField()
    AQI_yellow_days = models.IntegerField()
    AQI_orange_days = models.IntegerField()
    AQI_red_days = models.IntegerField()
    AQI_purple_days = models.IntegerField()
    AQI_maroon_days = models.IntegerField()
    binary_raw_file = models.BinaryField(null=True)

