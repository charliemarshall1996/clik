
import math
import requests


def get_coordinates(street, city, county, postalcode, country="United Kingdom"):
    url = 'https://nominatim.openstreetmap.org/search?'
    params = {
        'street': street,
        'city': city,
        'county': county,
        'country': country,
        'postalcode': postalcode,
        'format': 'json',
        'addressdetails': 1,
        'limit': 1  # Only get the top result
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return float(latitude), float(longitude)
        else:
            print("No results found.")
    else:
        print(f"Error: {response.status_code}")
    return None


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
