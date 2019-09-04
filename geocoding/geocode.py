from django_air_quality.privatesettings import GOOGLE_API_KEY
from django.core.cache import cache
from django_air_quality.settings import CACHE_TIMEOUT_SECONDS
import googlemaps

def get_latitude_longitude_for_zipcode(zipcode):

    """
    given a zipcode, checks cache for existing latitude/longitude
    if not found, calls get_latitude_longitude_from_google_maps
    """

    cached_value = cache.get(str(zipcode))
    if cached_value is not None:
        lat_long = cached_value.split("/")
        latitude = lat_long[0]
        longitude = lat_long[1]
        return latitude, longitude
    else:
        success, lat_long = get_latitude_longitude_from_google_maps(zipcode)
        if not success:
            raise Exception('"DEBUG: could not retrieve latitude and longitude from gmaps API for zipcode {0} for reason: {1}'.format(zipcode,lat_long))
        latitude = lat_long[0]
        longitude = lat_long[1]
        cache.set(str(zipcode), str("{0}/{1}".format(latitude,longitude)), timeout=CACHE_TIMEOUT_SECONDS)
        return latitude, longitude


def get_latitude_longitude_from_google_maps(zipcode):
    """
    Attempts to extract a latitude and longitude from google's geocoding API for a provided zipcode
    :param zipcode: zipcode to search for
    :return: (true, [latitude,longitude]) if successful. Returns (false, error_message) if unsuccesful
    """

    print("querying {0} for latitude and longitude from google geocode".format(zipcode))
    key = GOOGLE_API_KEY

    try:
        gm = googlemaps.Client(key=key)
    except ValueError:
        return False, 'invalid google geocoding API credentials'

    try:
        result = gm.geocode(zipcode)
    except googlemaps.exceptions.ApiError or googlemaps.exceptions.Timeout or \
           googlemaps.exceptions.HTTPError or googlemaps.exceptions.TransportError as err:
        return False, 'error looking up zipcode with google geocoding API {}'.format(err)

    try:
        latitude = result[0]['geometry']['location']['lat']
        longitude = result[0]['geometry']['location']['lng']

        if not latitude or not longitude:
            return False, 'could not get lat/lng coordinates. google maps geocode lookup returned {}'.format(
                result)

    except IndexError:
        return False, 'could not extract location and longitude from geocoding response {}'.format(result)

    return True, [latitude, longitude]

