
import math
import time

from django.conf import settings
from django.utils import timezone
from opencage.geocoder import OpenCageGeocode

from .models import OpenCageAPIRequest

geocoder = OpenCageGeocode(settings.OPEN_CAGE_KEY)


def get_coordinates(street, city, county, postalcode, country="United Kingdom"):
    now = timezone.now()
    last_request = OpenCageAPIRequest.objects.last()
    if last_request and last_request.last_request:
        # Calculate the time difference
        time_since_last_request = (
            now - last_request.last_request).total_seconds()

        # If the last request was less than 1 second ago, wait for the remainder
        if time_since_last_request < 1:
            time.sleep(1 - time_since_last_request)

    if not last_request:
        last_request = OpenCageAPIRequest.objects.create()

    query = f"{street}, {city}, {county}, {postalcode}, {country}"

    result = geocoder.geocode(query)

    last_request.last_request = now
    last_request.save()

    return float(result[0]['geometry']['lat']), float(result[0]['geometry']['lng']) if result else None


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * \
        math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
