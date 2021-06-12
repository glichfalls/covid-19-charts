import requests
from contextlib import closing
import csv
import codecs
from models.case import Case
from db import DatabaseConnection
import config

# config
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'

# db connection
db = DatabaseConnection(
    config.db_credentials['host'],
    config.db_credentials['database'],
    config.db_credentials['user'],
    config.db_credentials['password']
)

continents: list = db.get_continents()
countries: list = db.get_countries()

print(continents)
print(countries)

# empty cases table
db.truncate_cases()

# load csv
with closing(requests.get(url, stream=True)) as r:
    reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',')
    next(reader)
    for row in reader:

        if row[1] == "":
            continue

        # insert continent if not present already
        if not any(continent[1] == row[1] for continent in continents):
            con_id: int = db.insert_content(row[1])
            print("con id: " + str(con_id))
            continents.append([con_id, row[1]])

        continent_id: int = [x for x in continents if x[1] == row[1]][0][0]

        if not any(country[2] == row[0] for country in countries):
            print(continent_id, row[0], row[2])
            cty_id: int = db.insert_country(continent_id, row[0], row[2])
            print("cty id: " + str(cty_id))
            countries.append([cty_id, continent_id, row[0], row[2]])

        country_id: int = [x for x in countries if x[2] == row[0]][0][0]

        # insert case
        case: Case = Case.from_row(country_id, row)
        print(case.to_list())
        db.insert_case(case)

db.commit()
