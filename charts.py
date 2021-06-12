import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from db import DatabaseConnection
from datetime import datetime


class Charts:

    def __init__(self, db: DatabaseConnection):
        self._db = db

    # get pie chart of the total cases by continent and of the given date
    def show_pie_of_total_cases_by_continent(self, date: str = None):
        if date is None:
            date = datetime.today().strftime('%Y-%m-%d')
        # load continent labels
        labels = [country[1] for country in self._db.get_continents()]
        # load cases by continent
        sizes = [case[1] for case in self._db.get_continent_cases(date)]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax1.axis('equal')
        plt.show()

    def show_line_total_cases(self):
        cases = self._db.get_total_cases()
        vaccines = self._db.get_total_vaccinations()
        labels = [datetime.strptime(x[0], '%Y-%m-%d') for x in cases]
        plt.plot(labels, [x[1] for x in cases])
        plt.plot(labels, [x[2] for x in cases])
        plt.plot(labels, [x[1] for x in vaccines])
        plt.title('total worldwide cases')
        plt.gcf().autofmt_xdate()
        plt.gca().yaxis.set_major_formatter(ticker.EngFormatter())
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.grid(True)
        plt.show()
