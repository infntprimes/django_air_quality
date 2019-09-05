from google.cloud import bigquery
import csv

"""
contains queries for BigQuery module to run
"""

raw_air_quality_query = """
#standardSQL
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
  ABS(33.3 - latitude) + ABS(-111.5 - longitude) AS closest
FROM
  `bigquery-public-data.epa_historical_air_quality.pm25_frm_daily_summary`
WHERE
  latitude > @user_latitude - 1
  AND latitude < @user_latitude + 1
  AND longitude > @user_longitude - 1
  AND longitude < @user_longitude + 1
  AND sample_duration = "24 HOUR"
  AND poc = 1
  AND date_local <= '2016-01-01'
  AND date_local >= '2015-01-01'
ORDER BY
  1 DESC )) WHERE rnk = 1
"""

