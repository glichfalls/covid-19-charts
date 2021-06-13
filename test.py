import config
import getopt
import sys
from charts import Charts
from db import DatabaseConnection

db = DatabaseConnection(
    config.db_credentials['host'],
    config.db_credentials['database'],
    config.db_credentials['user'],
    config.db_credentials['password']
)


def get_help():
    print('covid-19 charts')
    print('help: show this help')
    print('exit: stop the application')
    print('1: show total cases by continent')


if __name__ == "__main__":
    try:

        action = None

        charts = Charts(db)

        # infinite loop until exit
        while True:

            # get user input for action
            action = input('enter your option:')

            if action == 'help':
                get_help()
            if action == '1':
                charts.show_pie_of_total_cases_by_continent()
            if action == '2':
                pass
            elif action == 'exit':
                sys.exit(0)

    except getopt.error as err:
        print(str(err))
        sys.exit(2)
