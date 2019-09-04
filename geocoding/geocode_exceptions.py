class GoogleGeocodeException(Exception):
    """Base class for geocode exceptions"""

class ClientConnectionException(GoogleGeocodeException):
    """
    Raised when the googlemaps Client cannot be authenticated or initialized
    """
    pass

class GeocodingLatitudeLongitudeIndexError(Exception):
    """
    raised when a lat/long can't be extracted from google's geocoding API response
    typically, this indicates that the format of a response from google's geocoding API has changed
    """
    pass

class GeocodingLatitudeLongitudeNotFoundError(Exception):
    """
    raised when lat/long are blank in a response from google's geocoding API
    """
    pass

