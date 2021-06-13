import pyodbc
from models.case import Case
from models.vaccination import Vaccination
from models.test import Test


class DatabaseConnection:
    conn = None
    cursor = None

    def __init__(self, server: str, db: str, user: str, password: str):
        connection_string: str = 'DRIVER={{SQL Server}};SERVER={0};DATABASE={1};UID={2};PWD={3};Trusted_Connection=yes;'
        self.conn = pyodbc.connect(connection_string.format(server, db, user, password))
        self.cursor = self.conn.cursor()

    def truncate_countries(self):
        self.cursor.execute("truncate table Country")
        self.cursor.commit()

    def truncate_continents(self):
        self.cursor.execute("truncate table Continent")
        self.cursor.commit()

    def truncate_cases(self):
        self.cursor.execute("truncate table Cases")
        self.cursor.commit()

    def truncate_tests(self):
        self.cursor.execute("truncate table Tests")
        self.cursor.commit()

    def truncate_vaccinations(self):
        self.cursor.execute("truncate table Vaccinations")
        self.cursor.commit()

    def get_continents(self):
        self.cursor.execute("select * from Continent order by con_id")
        return self.cursor.fetchall()

    def get_countries(self):
        self.cursor.execute("select * from Country")
        return self.cursor.fetchall()

    def insert_content(self, name: str) -> int:
        sql = """
        declare @out int;
        exec create_continent @name = ?, @new_identity = @out output;
        select @out AS the_output;
        """
        self.cursor.execute(sql, name)
        inserted_id: int = self.cursor.fetchall()
        self.commit()
        return inserted_id[0][0]

    def insert_country(self, con_id: int, iso: str, name: str, population: int) -> int:
        sql = """
        declare @out int;
        exec create_country @continent = ?, @iso_code = ?, @name = ?, @population = ?, @new_identity = @out output;
        select @out as the_output;
        """
        self.cursor.execute(sql, (con_id, iso, name, population))
        inserted_id: int = self.cursor.fetchall()
        self.commit()
        return inserted_id[0][0]

    def insert_case(self, case: Case):
        sql = "exec create_cases @country = ?, @date = ?, @total_cases = ?, @new_cases = ?, @total_deaths = ?, @new_deaths = ?, @reproduction_rate = ?;"
        self.cursor.execute(sql, case.to_tuple())
        self.commit()

    def insert_vaccinations(self, vaccination: Vaccination):
        sql = "exec create_vaccinations @country = ?, @date = ?, @total_vaccinations = ?, @people_vaccinated = ?, @people_fully_vaccinated = ?, @new_vaccinations = ?;"
        self.cursor.execute(sql, vaccination.to_tuple())
        self.commit()

    def insert_tests(self, test: Test):
        sql = "exec create_tests @country = ?, @date = ?, @new_tests = ?, @total_tests = ?, @positive_rate = ?;"
        self.cursor.execute(sql, test.to_tuple())
        self.commit()

    def get_continent_cases(self, date: str):
        sql = """
        select con.con_id, sum(cas_total_cases) as total_cases from Cases cas
        join Country cou on cas.cty_id = cou.cty_id
        join Continent con on con.con_id = cou.con_id
        where cas_date = ?
        group by con.con_id, cas_date
        order by con.con_id
        """
        self.cursor.execute(sql, date)
        return self.cursor.fetchall()

    def get_total_cases(self):
        sql = "select cas_date, sum(cas_total_cases), sum(cas_total_deaths) from Cases group by cas_date order by cas_date"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_total_vaccinations(self):
        sql = "select vac_date, sum(cast(vac_total_vaccinations as bigint)) from Vaccinations group by vac_date order by vac_date"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def commit(self):
        self.cursor.commit()
