from background_task import background
from django.contrib.auth.models import User
from .models import Report, ZipcodeLatLong
from datetime import datetime, timedelta
from geocoding.geocode import get_latitude_longitude_for_zipcode

import json

def create_report(request_body):
    """
    responsible for creating a report, called by our task queue's generate_report_handler
    """
    report_json = json.loads(request_body)
    zipcode = report_json['zipcode']
    start_date = report_json['start_date']
    end_date = report_json['end_date']

    latitude, longitude = get_latitude_longitude_for_zipcode(zipcode)






