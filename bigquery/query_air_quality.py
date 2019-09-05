from google.cloud import bigquery
import django_air_quality.privatesettings
from bigquery.queries import raw_air_quality_query

def retrieve_raw_air_quality_data(latitude,longitude,start_date,end_date):
    """
    initializies and runs queries
    """
    client = bigquery.Client()
    query_params = [
        bigquery.ScalarQueryParameter("user_latitude", "FLOAT", latitude),
        bigquery.ScalarQueryParameter("user_longitude", "FLOAT", longitude),
        bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
        bigquery.ScalarQueryParameter("end_date", "DATE", end_date)
    ]
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = query_params
    query_job = client.query(raw_air_quality_query, location="US", job_config=job_config)

    return query_job