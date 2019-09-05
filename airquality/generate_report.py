from background_task import background
from django.contrib.auth.models import User
from .models import Report
from datetime import datetime, timedelta
from geocoding.geocode import get_latitude_longitude_for_zipcode
from bigquery import query_air_quality
from airquality import create_report_from_raw_data
import json

def create_report(request_body):
    """
    responsible for creating a report, called by our task queue's generate_report_handler
    """
    report_json = json.loads(request_body)
    zipcode = report_json['zipcode']
    start_date = report_json['start_date']
    end_date = report_json['end_date']

    #get latitude and longitude
    latitude, longitude = get_latitude_longitude_for_zipcode(zipcode)

    #pass relevant parameters to run a query against epa historical records
    query_report = query_air_quality.retrieve_raw_air_quality_data(latitude,longitude,start_date,end_date)

    #parse the results and commit as a model to our db
    create_report_from_raw_data.create_report_from_raw_data(query_report, zipcode, start_date, end_date)






