from django_air_quality.privatesettings import GOOGLE_API_KEY
from django.core.cache import cache
from django_air_quality.settings import CACHE_TIMEOUT_SECONDS
import googlemaps
from geocoding.geocode_exceptions import ClientConnectionException,GeocodingLatitudeLongitudeIndexError, GeocodingLatitudeLongitudeNotFoundError

def get_latitude_longitude_for_zipcode(zipcode):

    """
    given a zipcode, checks cache for existing latitude/longitude
    if not found, calls get_latitude_longitude_from_google_maps
    """
    cached_value = cache.get(str(zipcode))
    if cached_value is not None:
        latitude, longitude = cached_value.split("/")
        return latitude, longitude
    else:
        latitude, longitude = get_latitude_longitude_from_google_maps(zipcode)
        cache.set(str(zipcode), str("{0}/{1}".format(latitude,longitude)), timeout=CACHE_TIMEOUT_SECONDS)
        return latitude, longitude


def get_latitude_longitude_from_google_maps(zipcode):
    """
    Attempts to extract a latitude and longitude from google's geocoding API for a provided zipcode
    :param zipcode: zipcode to search for
    :return: latitude, longitude
    """

    print("querying {0} for latitude and longitude from google geocode".format(zipcode))
    key = GOOGLE_API_KEY

    try:
        gm = googlemaps.Client(key=key)
    except ValueError:
        raise ClientConnectionException('invalid google geocoding API credentials')

    try:
        result = gm.geocode(zipcode)
    except googlemaps.exceptions.ApiError or googlemaps.exceptions.Timeout or \
           googlemaps.exceptions.HTTPError or googlemaps.exceptions.TransportError as err:
        raise err('error looking up zipcode with google geocoding API {}'.format(err))

    try:
        latitude = result[0]['geometry']['location']['lat']
        longitude = result[0]['geometry']['location']['lng']

    except IndexError:
        raise GeocodingLatitudeLongitudeIndexError('could not extract location and longitude from geocoding response {}'.format(result))

    if not latitude or not longitude:
        raise GeocodingLatitudeLongitudeNotFoundError('could not get lat/lng coordinates. google maps geocode lookup returned {}'.format(
                result))

    return latitude, longitude
