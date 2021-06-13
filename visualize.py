import config
from charts import Charts
from db import DatabaseConnection

db = DatabaseConnection(
    config.db_credentials['host'],
    config.db_credentials['database'],
    config.db_credentials['user'],
    config.db_credentials['password']
)

charts = Charts(db)

charts.show_case_death_chart()