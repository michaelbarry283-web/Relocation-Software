import re
import json
import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from models import Country
from gemini_service import generate_travel_guide


# =========================================
# Save Directory
# =========================================

SAVE_DIR = Path("saved_data")
SAVE_DIR.mkdir(exist_ok=True)


# =========================================
# Relocation Guide Generator
# =========================================

class RelocationGuide:
    def generate(self, country):
        try:
            if not isinstance(country, Country):
                raise TypeError("Expected a Country object")
            ai_text = generate_travel_guide(country)

            if not ai_text:
                ai_text = "No AI guide available. Please try again."

            guide = {
                "title": f"Relocation Guide: {country.name}",
                "summary": ai_text,
                "details": {
                    "capital": country.capital,
                    "region": country.region,
                    "timezone": ", ".join(country.timezone),
                    "population": country.population
                },
                "travel_checklist": [
                    "Research visa requirements",
                    "Learn local customs",
                    "Prepare for timezone adjustments"
                ]
            }

            return guide

        except Exception as e:
            return {
                "title": "Error",
                "summary": f"Something went wrong: {str(e)}",
                "details": {},
                "travel_checklist": []
            }


# =========================================
# Country Comparator
# =========================================

class CountryComparator:

    def compare(self, country1, country2):

        try:
            if not isinstance(country1, Country) or not isinstance(country2, Country):
                raise TypeError("Both inputs must be Country objects")

            if country1.population > country2.population:
                population_result = (
                    f"{country1.name} has a larger population."
                )

            elif country2.population > country1.population:
                population_result = (
                    f"{country2.name} has a larger population."
                )

            else:
                population_result = (
                    "Both countries have the same population."
                )

            comparison = {
                "title": f"{country1.name} vs {country2.name}",

                "country_1": {
                    "name": country1.name,
                    "capital": country1.capital,
                    "currency": country1.currency,
                    "languages": ", ".join(country1.languages),
                    "population": country1.population,
                    "region": country1.region,
                    "timezone": ", ".join(country1.timezone)
                },

                "country_2": {
                    "name": country2.name,
                    "capital": country2.capital,
                    "currency": country2.currency,
                    "languages": ", ".join(country2.languages),
                    "population": country2.population,
                    "region": country2.region,
                    "timezone": ", ".join(country2.timezone)
                },

                "population_comparison": population_result
            }

            return comparison

        except Exception as e:
            return {"error": str(e)}


# =========================================
# Travel Checklist Generator
# =========================================

class TravelChecklistGenerator:

    BASE_CHECKLIST = {
        "Documents": [
            "Valid passport",
            "Visa or entry permit",
            "Travel insurance",
            "Accommodation bookings",
            "Emergency contact list"
        ],

        "Health & Safety": [
            "Basic first-aid kit",
            "Prescription medicines",
            "Research nearby hospitals"
        ],

        "Money & Finance": [
            "Exchange local currency",
            "Notify bank before travel",
            "Keep emergency cash"
        ],

        "Connectivity": [
            "Check roaming availability",
            "Buy local SIM or eSIM",
            "Download offline maps"
        ],

        "Packing": [
            "Weather-appropriate clothing",
            "Power adapter",
            "Copies of important documents"
        ]
    }

    def __init__(self, country):

        if not isinstance(country, Country):
            raise TypeError("Expected a Country object")

        self.country = country

    def generate(self):

        checklist = dict(self.BASE_CHECKLIST)

        checklist["Country Information"] = [
            f"Capital: {self.country.capital}",
            f"Currency: {self.country.currency}",
            f"Languages: {', '.join(self.country.languages)}",
            f"Timezone: {', '.join(self.country.timezone)}"
        ]

        return {
            "country": self.country.name,
            "generated": datetime.datetime.now().isoformat(),
            "checklist": checklist
        }

    def save(self):

        result = self.generate()

        safe_name = re.sub(r"[^\w\-]", "_", self.country.name)

        filepath = SAVE_DIR / f"checklist_{safe_name}.json"

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4)

        return filepath

    def display(self):

        result = self.generate()

        lines = [
            f"\nBefore You Travel to {result['country']}",
            "=" * 50
        ]

        for section, items in result["checklist"].items():

            lines.append(f"\n{section}")

            for item in items:
                lines.append(f" - {item}")

        return "\n".join(lines)


# =========================================
# Timezone Difference Calculator
# =========================================

class TimezoneCalculator:

    def __init__(self, country1, country2):

        if not isinstance(country1, Country) or not isinstance(country2, Country):
            raise TypeError("Both inputs must be Country objects")

        self.country1 = country1
        self.country2 = country2

    def timezone_to_offset(self, timezone_string):

        if not timezone_string or not isinstance(timezone_string, str):
            raise ValueError(f"Invalid timezone format: {timezone_string}")

        timezone_string = timezone_string.strip()

        if timezone_string == "UTC":
            return datetime.timedelta()

        match = re.match(r"UTC([+-])(\d{2}):(\d{2})", timezone_string)

        if not match:
            raise ValueError(f"Invalid timezone format: {timezone_string}")

        sign, hours, minutes = match.groups()

        delta = datetime.timedelta(
            hours=int(hours),
            minutes=int(minutes)
        )

        return delta if sign == "+" else -delta

    def calculate(self):

        tz1 = self.country1.timezone
        tz2 = self.country2.timezone

        if isinstance(tz1, list):
            tz1 = tz1[0] if tz1 else "UTC"

        if isinstance(tz2, list):
            tz2 = tz2[0] if tz2 else "UTC"

        try:
            offset1 = self.timezone_to_offset(tz1)
        except ValueError:
            offset1 = datetime.timedelta()

        try:
            offset2 = self.timezone_to_offset(tz2)
        except ValueError:
            offset2 = datetime.timedelta()

        difference = offset2 - offset1

        difference_hours = difference.total_seconds() / 3600

        if difference_hours > 0:
            message = (
                f"{self.country2.name} is "
                f"{difference_hours} hour(s) ahead of "
                f"{self.country1.name}."
            )

        elif difference_hours < 0:
            message = (
                f"{self.country2.name} is "
                f"{abs(difference_hours)} hour(s) behind "
                f"{self.country1.name}."
            )

        else:
            message = (
                f"{self.country1.name} and "
                f"{self.country2.name} share the same timezone."
            )

        return {
            "country_1": self.country1.name,
            "country_2": self.country2.name,
            "timezone_1": tz1,
            "timezone_2": tz2,
            "difference_hours": difference_hours,
            "message": message
        }

    def display(self):

        result = self.calculate()

        return (
            f"\nTimezone Comparison\n"
            f"{'=' * 50}\n"
            f"{result['country_1']} : {result['timezone_1']}\n"
            f"{result['country_2']} : {result['timezone_2']}\n"
            f"Difference: {result['difference_hours']} hour(s)\n"
            f"{result['message']}"
        )