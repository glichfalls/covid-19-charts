

class Test:

    def __init__(self, country: int, date: str, new_tests: int, total_tests: int, positive_rate: float):
        self._country = country
        self._date = date
        self._new_tests = new_tests
        self._total_tests = total_tests
        self._positive_rate = positive_rate

    @staticmethod
    def from_row(country: int, row: list):
        return Test(
            country,
            row[3],
            int(float(row[25] or 0)),
            int(float(row[26] or 0)),
            float(row[31] or 0),
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
    def date(self, date: int):
        self._date = date

    @property
    def new_tests(self) -> int:
        return self._new_tests

    @new_tests.setter
    def new_tests(self, new_tests: int):
        self._new_tests = new_tests

    @property
    def total_tests(self) -> int:
        return self._total_tests

    @total_tests.setter
    def total_tests(self, total_tests: int):
        self._total_tests = total_tests

    @property
    def positive_rate(self) -> float:
        return self._positive_rate

    @positive_rate.setter
    def positive_rate(self, positive_rate: float):
        self._positive_rate = positive_rate

    def to_tuple(self) -> tuple:
        return (
            self.country,
            self.date,
            self.new_tests,
            self.total_tests,
            self.positive_rate
        )
