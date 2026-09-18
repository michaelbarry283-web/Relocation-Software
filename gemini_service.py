import google.generativeai as genai

# Replace with your actual API key
genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-2.0-flash")


def generate_travel_guide(country):

    prompt = f"""
You are a travel and relocation advisor.

Generate a simple relocation guide for:

Country: {country.name}
Capital: {country.capital}
Region: {country.region}
Population: {country.population}
Languages: {", ".join(country.languages)}
Timezone: {", ".join(country.timezone)}

Include:
- lifestyle
- culture
- travel tips
- adaptation advice
- pros and challenges

Keep it concise and student-friendly.
"""

    response = model.generate_content(prompt)

    return response.text