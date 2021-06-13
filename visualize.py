from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt

import config
from db import DatabaseConnection

# db connection
db = DatabaseConnection(
    config.db_credentials['host'],
    config.db_credentials['database'],
    config.db_credentials['user'],
    config.db_credentials['password']
)

# Pie chart
def create_continent_chart():
    dbData = db.get_continents()

    continent = [x[1] for x in dbData]
    sizes = [15, 30, 45, 10, 1, 10]
    explode = (0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=continent, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

def create_case_chart():
    dbData = db.get_cases()
    dt = datetime.today() - timedelta(days=1)
    dateList = [x[2] for x in dbData]
    dateList = dateList[:dateList.index(dt.strftime('%Y-%m-%d')) + 1]
    del dateList[::2]
    del dateList[::2]
    del dateList[::2]
    del dateList[::2]

    caseList = []
    deathList = []

    for i in dateList:
        tempCaseList = [x[3] for x in dbData if x[2] == i]
        tempDeathList = [x[5] for x in dbData if x[2] == i]
        tempCases = 0
        tempDeaths = 0

        for j in tempCaseList:
            tempCases = tempCases + j
        caseList.append(tempCases / 1000000)

        for j in tempDeathList:
            tempDeaths = tempDeaths + j
        deathList.append(tempDeaths / 1000000)

    Date = dateList
    Cases = caseList
    Deaths = deathList

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Datum')
    ax1.set_ylabel('Fälle in mio', color=color)
    ax1.plot(Date, Cases, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Gestorbene in mio', color=color)  # we already handled the x-label with ax1
    ax2.plot(Date, Deaths, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.show()


#create_continent_chart()
create_case_chart()