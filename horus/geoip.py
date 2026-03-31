import geoip2.database
import os

BASE_DIR = os.path.dirname(__file__)
db_path = os.path.join(BASE_DIR, "GeoLite2-City.mmdb")

reader = None

# تحميل الداتابيز بشكل آمن
if os.path.exists(db_path):
    try:
        reader = geoip2.database.Reader(db_path)
    except Exception:
        reader = None
else:
    print("[WARNING] GeoIP database not found. Location data will be unavailable.")


def get_ip_info(ip):
    # لو مفيش reader
    if reader is None:
        return {
            "country": "Unknown",
            "city": "Unknown"
        }

    try:
        response = reader.city(ip)

        country = response.country.name or "Unknown"
        city = response.city.name or "Unknown"

        return {
            "country": country,
            "city": city
        }

    except Exception:
        return {
            "country": "Unknown",
            "city": "Unknown"
        }