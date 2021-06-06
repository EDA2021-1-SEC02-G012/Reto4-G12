from geopy.geocoders import Nominatim


def findCountry(coordinates):
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.reverse(coordinates)
    return location.raw
