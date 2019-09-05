from google.cloud import bigquery
import csv

"""
contains queries for BigQuery module to run
"""

raw_air_quality_query = """
#standardSQL
SELECT date_local, aqi, AQ_RATING, parameter_name, latitude, longitude, address, city_name, state_name FROM (
SELECT * FROM (
SELECT *, RANK() OVER (Partition BY date_local ORDER BY closest ASC) as rnk
FROM (
#standardSQL
SELECT
  date_local,
  latitude,
  longitude,
  address,
  city_name,
  state_name,
  parameter_name,
  CASE
    WHEN aqi < 51 THEN "Good (green)"
    WHEN aqi <101 THEN "Moderate (yellow)"
    WHEN aqi <151 THEN "Unhealthy for sensitive groups (orange)"
    WHEN aqi <201 THEN "Unhealthy (red)"
    WHEN aqi <301 THEN "Very unhealthy (purple)"
    WHEN aqi <501 THEN "Hazardous (maroon)"
    ELSE "unexpected data"
  END AS AQ_RATING,
  aqi,
  ABS(@user_latitude - latitude) + ABS(@user_longitude - longitude) AS closest
FROM
  `bigquery-public-data.epa_historical_air_quality.pm25_frm_daily_summary`
WHERE
  latitude > @user_latitude - 1
  AND latitude < @user_latitude + 1
  AND longitude > @user_longitude - 1
  AND longitude < @user_longitude + 1
  AND sample_duration = "24 HOUR"
  AND poc = 1
  AND date_local <= @end_date
  AND date_local >= @start_date
ORDER BY
  1 DESC )) WHERE rnk = 1 )
"""

