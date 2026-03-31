import geoip2.database
import os

BASE_DIR = os.path.dirname(__file__)
db_path = os.path.join(BASE_DIR, "GeoLite2-City.mmdb")

reader = geoip2.database.Reader(db_path)

def get_ip_info(ip):
    try:
        response = reader.city(ip)

        country = response.country.name
        city = response.city.name

        return {
            "country": country,
            "city": city
        }

    except:
        return {
            "country": "Unknown",
            "city": "Unknown"
        }