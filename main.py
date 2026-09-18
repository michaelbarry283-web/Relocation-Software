import streamlit as st

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F0F8FF;
    }

    section[data-testid="stSidebar"] {
        background-color: #E6F2FF;
    }

    h1, h2, h3 {
        color: #1E90FF;
    }

    .stButton>button {
        background-color: #1E90FF;
        color: white;
        border-radius: 8px;
    }

    .stButton>button:hover {
        background-color: #00BFFF;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

from api import get_country
from services import (
    RelocationGuide,
    CountryComparator,
    TravelChecklistGenerator,
    TimezoneCalculator
)
from storage import StorageManager


# =========================
# Setup
# =========================

st.set_page_config(page_title="Country Relocation Guide", layout="wide")

storage = StorageManager()
FAV_FILE = "favorites.json"


# =========================
# Helper
# =========================

def fetch_country(name):
    country = get_country(name)
    return country


def save_favorite(country):
    storage.append(FAV_FILE, {
        "name": country.name,
        "capital": country.capital,
        "currency": country.currency,
        "region": country.region,
        "flag": country.flag
    })


# =========================
# UI
# =========================

st.title("🌍 Country Relocation & Culture Guide")

menu = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Search Country",
        "Compare Countries",
        "Travel Checklist",
        "Timezone Difference",
        "Favorites"
    ]
)

# =========================
# 1. SEARCH COUNTRY + GUIDE
# =========================

if menu == "Search Country":

    st.header("🔎 Search Country")

    name = st.text_input("Enter country name")

    if st.button("Search"):

        country = fetch_country(name)

        if not country:
            st.error("Country not found")
        else:
            st.success(country.name)

            st.image(country.flag)

            st.write("### Details")
            st.write(f"Capital: {country.capital}")
            st.write(f"Currency: {country.currency}")
            st.write(f"Region: {country.region}")
            st.write(f"Population: {country.population}")
            st.write(f"Languages: {', '.join(country.languages)}")
            st.write(f"Timezone: {', '.join(country.timezone)}")

            guide = RelocationGuide().generate(country)

            st.write("### 🧭 Relocation Guide")
            st.write(guide["summary"])

            for k, v in guide["details"].items():
                st.write(f"**{k}:** {v}")

            st.write("### 🧳 Checklist")
            for item in guide["travel_checklist"]:
                st.write(f"- {item}")

            if st.button("⭐ Save to Favorites"):
                save_favorite(country)
                st.success("Saved!")


# =========================
# 2. COMPARE COUNTRIES
# =========================

elif menu == "Compare Countries":

    st.header("⚖️ Compare Countries")

    c1 = st.text_input("Country 1")
    c2 = st.text_input("Country 2")

    if st.button("Compare"):

        country1 = fetch_country(c1)
        country2 = fetch_country(c2)

        if not country1 or not country2:
            st.error("Invalid country input")
        else:

            result = CountryComparator().compare(country1, country2)

            st.subheader(result["title"])

            col1, col2 = st.columns(2)

            with col1:
                st.write("### Country 1")
                st.write(result["country_1"])

            with col2:
                st.write("### Country 2")
                st.write(result["country_2"])

            st.info(result["population_comparison"])


# =========================
# 3. TRAVEL CHECKLIST
# =========================

elif menu == "Travel Checklist":

    st.header("🧳 Travel Checklist")

    name = st.text_input("Enter country name")

    if st.button("Generate Checklist"):

        country = fetch_country(name)

        if country:

            checklist = TravelChecklistGenerator(country)

            result = checklist.generate()

            st.subheader(f"Checklist for {result['country']}")

            for section, items in result["checklist"].items():

                st.write(f"### {section}")

                for item in items:
                    st.write(f"- {item}")

        else:
            st.error("Country not found")


# =========================
# 4. TIMEZONE DIFFERENCE
# =========================

elif menu == "Timezone Difference":

    st.header("🕐 Timezone Comparison")

    c1 = st.text_input("Country 1")
    c2 = st.text_input("Country 2")

    if st.button("Calculate"):

        country1 = fetch_country(c1)
        country2 = fetch_country(c2)

        if country1 and country2:

            calc = TimezoneCalculator(country1, country2)

            result = calc.calculate()

            st.subheader("Result")
            st.write(result["message"])

        else:
            st.error("Invalid countries")


# =========================
# 5. FAVORITES
# =========================

elif menu == "Favorites":

    st.header("⭐ Favorites")

    data = storage.load(FAV_FILE)

    if not data:
        st.info("No favorites saved yet.")
    else:
        for item in data:
            st.write(f"**{item['name']}**")
            st.write(f"Capital: {item['capital']}")
            st.write(f"Currency: {item['currency']}")
            st.write("---")