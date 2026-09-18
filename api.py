import requests 
import re
from models import Country

BASE_URL = "https://restcountries.com/v3.1/name/"


def validate_country_name(name):
    """
    Validates country name using regex.
    Allows letters, spaces, and hyphens only.
    """
    pattern = r"^[A-Za-z\s\-]+$"
    return bool(re.match(pattern, name))


def get_country(country_name):
    """
    Fetch country data and return a Country object.
    Returns None if country is invalid or not found.
    """

    if not validate_country_name(country_name):
        print("❌ Invalid country name format.")
        return None

    try:
        response = requests.get(BASE_URL + country_name, timeout=5)

        if response.status_code != 200:
            print("❌ Country not found.")
            return None

        data = response.json()[0]

        name = data.get("name", {}).get("common", "N/A")

        capital = data.get("capital", ["N/A"])
        capital = capital[0] if capital else "N/A"

        currencies = data.get("currencies", {})
        currency = list(currencies.keys())[0] if currencies else "N/A"

        languages_dict = data.get("languages", {})
        languages = list(languages_dict.values()) if languages_dict else ["N/A"]

        population = data.get("population", 0)

        region = data.get("region", "N/A")

        flag = data.get("flags", {}).get("png", "N/A")

        timezone = data.get("timezones", [])
        timezone = ", ".join(timezone)

        country = Country(
            name=name,
            capital=capital,
            currency=currency,
            languages=languages,
            population=population,
            region=region,
            flag=flag,
            timezone=timezone
        )

        return country

    except requests.exceptions.RequestException:
        print("❌ Network error. Please check your internet.")
        return None

    except (KeyError, IndexError, TypeError):
        print("❌ Error processing country data.")
        return None