import csv
import io
import sys
from google.cloud import bigquery
from .models import AirQualityReport
from django.core.files.uploadedfile import InMemoryUploadedFile
import unicodedata

def create_report_from_raw_data(query_job):
    """
    creates and saves an AirQualityReport model to the database, takes the output of a query as an input
    """
    #get data for table
    green_count = 0
    yellow_count = 0
    orange_count = 0
    red_count = 0
    purple_count = 0
    maroon_count = 0

    for row in query_job:
        if 'green' in str(row[2]):
            green_count += 1

        elif 'yellow' in str(row[2]):
            yellow_count +=1

        elif 'orange' in str(row[2]):
            orange_count +=1

        elif 'red' in str(row[2]):
            red_count +=1

        elif 'purple' in str(row[2]):
            purple_count +=1

        elif 'maroon' in str(row[2]):
            maroon_count += 1

    print('a')

    in_memory_csv = io.StringIO()
    writer = csv.writer(in_memory_csv, quoting=csv.QUOTE_MINIMAL)
    for row in query_job:
        writer.writerow(row)
    in_memory_csv.seek(0)

    # in_memory_csv.seek(0,2)
    # django_file = InMemoryUploadedFile(in_memory_csv, "raw_data", "raw_data.csv", None, in_memory_csv.tell(), None)

    raw_data = (in_memory_csv.getvalue()).encode('utf-8')

    report = AirQualityReport.objects.create(
        AQI_green_days=green_count,
        AQI_yellow_days=yellow_count,
        AQI_orange_days=orange_count,
        AQI_red_days=red_count,
        AQI_purple_days=purple_count,
        AQI_maroon_days=maroon_count,
        binary_raw_file=raw_data
    )

    print("SAVING REPORT")

    report.save()