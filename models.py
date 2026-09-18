class Country:
    def __init__(self, name, capital, currency, languages,
                 population, region, flag, timezone):

        self.name = name
        self.capital = capital
        self.currency = currency
        self.languages = languages
        self.population = population
        self.region = region
        self.flag = flag
        self.timezone = timezone

    def __str__(self):
        return (
            f"Country: {self.name}\n"
            f"Capital: {self.capital}\n"
            f"Currency: {self.currency}\n"
            f"Languages: {', '.join(map(str, self.languages))}\n"
            f"Population: {self.population}\n"
            f"Region: {self.region}\n"
            f"Timezone: {', '.join(map(str, self.timezone))}\n"
            f"Flag: {self.flag}"
        )