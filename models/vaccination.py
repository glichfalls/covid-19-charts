

class Vaccination:

    def __init__(self, country: int, date: str, total_vaccinations: int, people_vaccinated: int, people_fully_vaccinated: int, new_vaccinations: int):
        self._country = country
        self._date = date
        self._total_vaccinations = total_vaccinations
        self._people_vaccinated = people_vaccinated
        self._people_fully_vaccinated = people_fully_vaccinated
        self._new_vaccinations = new_vaccinations

    @staticmethod
    def from_row(country: int, row: list):
        return Vaccination(
            country,
            row[3],
            int(float(row[34] or 0)),
            int(float(row[35] or 0)),
            int(float(row[36] or 0)),
            int(float(row[37] or 0)),
        )

    @property
    def country(self) -> int:
        return self._country

    @country.setter
    def country(self, country: int):
        self._country = country

    @property
    def date(self) -> str:
        return self._date

    @date.setter
    def date(self, date: str):
        self._date = date

    @property
    def total_vaccinations(self) -> int:
        return self._total_vaccinations

    @total_vaccinations.setter
    def total_vaccinations(self, total_vaccinations: int):
        self._total_vaccinations = total_vaccinations

    @property
    def people_vaccinated(self) -> int:
        return self._people_vaccinated

    @people_vaccinated.setter
    def people_vaccinated(self, people_vaccinated: int):
        self._people_vaccinated = people_vaccinated

    @property
    def people_fully_vaccinated(self) -> int:
        return self._people_fully_vaccinated

    @people_fully_vaccinated.setter
    def people_fully_vaccinated(self, people_fully_vaccinated: int):
        self._people_fully_vaccinated = people_fully_vaccinated

    @property
    def new_vaccinations(self) -> int:
        return self._new_vaccinations

    @new_vaccinations.setter
    def new_vaccinations(self, new_vaccinations: int):
        self._new_vaccinations = new_vaccinations

    def to_tuple(self) -> tuple:
        return (
            self.country,
            self.date,
            self.total_vaccinations,
            self.people_vaccinated,
            self.people_fully_vaccinated,
            self.new_vaccinations
        )
