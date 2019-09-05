import csv
import io
import sys
from google.cloud import bigquery
from .models import AirQualityReport, Report
from django.core.files.uploadedfile import InMemoryUploadedFile
import unicodedata


def create_report_from_raw_data(query_job, zipcode, start_date, end_date):
    """
    creates and saves an AirQualityReport model to the database, takes the output of a query as an input
    """
    # get data for table
    green_count = 0
    yellow_count = 0
    orange_count = 0
    red_count = 0
    purple_count = 0
    maroon_count = 0

    air_quality_dict = {
        'Good (green)': 0,
        'Moderate (yellow)': 0,
        'Unhealthy for sensitive groups (orange)': 0,
        'Unhealthy (red)': 0,
        'Very unhealthy(purple)': 0,
        'Hazardous(maroon)': 0,
    }

    for row in query_job:
        air_quality_dict[str(row[2])] += 1


    with io.StringIO() as in_memory_csv:
        writer = csv.writer(in_memory_csv, quoting=csv.QUOTE_MINIMAL)
        for row in query_job:
            writer.writerow(row)
        in_memory_csv.seek(0)
        raw_data = (in_memory_csv.getvalue()).encode('utf-8')

    report = AirQualityReport.objects.create(
        AQI_green_days=air_quality_dict['Good (green)'],
        AQI_yellow_days=air_quality_dict['Moderate (yellow)'],
        AQI_orange_days=air_quality_dict['Unhealthy for sensitive groups (orange)'],
        AQI_red_days=air_quality_dict['Unhealthy (red)'],
        AQI_purple_days=air_quality_dict['Very unhealthy(purple)'],
        AQI_maroon_days=air_quality_dict['Hazardous(maroon)'],
        binary_raw_file=raw_data,
        userRequest=Report.objects.get(zipcode=zipcode, start_date=start_date, end_date=end_date)
    )


    report.save()
