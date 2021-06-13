#!/usr/bin/python


import codecs
import config
import csv
import requests
import sys
import getopt
from contextlib import closing
from db import DatabaseConnection
from models.case import Case
from models.test import Test
from models.vaccination import Vaccination

# config
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'

# db connection
db = DatabaseConnection(
    config.db_credentials['host'],
    config.db_credentials['database'],
    config.db_credentials['user'],
    config.db_credentials['password']
)


def get_help():
    print('covid-19 charts database tool')
    print('usage: python fetcher.py ... [-v | -h | --verbose | --help]')
    print('options and arguments:')
    print('-v: display debug information (also --verbose)')
    print('-h: print this help message and exit (also --help)')


def rebuild_database(verbose: bool = False):
    if verbose:
        print('loading continent and country data')

    # load initial continent / country data
    continents: list = db.get_continents()
    countries: list = db.get_countries()

    if verbose:
        print('found {} continents and {} countries'.format(len(continents), len(countries)))

    if verbose:
        print('clearing database')

    db.truncate_cases()

    row_count: int = 0

    # load csv
    with closing(requests.get(url, stream=True)) as r:

        if verbose:
            print('loading csv rows')

        # read csv
        reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',')

        # skip header row
        next(reader)

        # iterate through all csv rows
        for index, row in enumerate(reader):

            row_count += 1

            if verbose:
                print('[{}] {}, {}'.format(index, row[2], row[3]))

            # skip row if continent is empty
            if row[1] == "":
                continue

            # insert continent if not present already
            if not any(continent[1] == row[1] for continent in continents):
                if verbose:
                    print('found new continent {}'.format(row[1]))
                con_id: int = db.insert_content(row[1])
                continents.append([con_id, row[1]])

            # get the continent id for the current row
            continent_id: int = [c for c in continents if c[1] == row[1]][0][0]

            if not any(country[2] == row[0] for country in countries):
                if verbose:
                    print('found new country {}'.format(row[2]))
                cty_id: int = db.insert_country(continent_id, row[0], row[2])
                countries.append([cty_id, continent_id, row[0], row[2]])

            # get the country id for the current row
            country_id: int = [c for c in countries if c[2] == row[0]][0][0]

            # insert case
            db.insert_case(Case.from_row(country_id, row))

            # create test
            db.insert_tests(Test.from_row(country_id, row))

            # create vaccination
            db.insert_vaccinations(Vaccination.from_row(country_id, row))

    if verbose:
        print('script finished, found {} rows'.format(row_count))


if __name__ == "__main__":
    try:

        # get cli arguments
        arguments, values = getopt.getopt(sys.argv[1:], "hv", ["help", "verbose"])

        # iterate through input arguments
        for argument, value in arguments:
            if argument in ("-h", "--help"):
                get_help()
                sys.exit(0)
            elif argument in ("-v", "--verbose"):
                rebuild_database(verbose=True)
                sys.exit(0)
            else:
                print("invalid parameter `" + argument + "`")
                sys.exit(2)

        # if no params available, start in silent mode
        rebuild_database(verbose=True)

    except getopt.error as err:
        print(str(err))
        sys.exit(2)
