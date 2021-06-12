import pyodbc
from models.case import Case


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

    def get_continents(self):
        self.cursor.execute("select * from Continent")
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
        self.cursor.commit()
        return inserted_id[0][0]

    def insert_country(self, con_id: int, iso: str, name: str) -> int:
        sql = """
        declare @out int;
        exec create_country @continent = ?, @iso_code = ?, @name = ?, @new_identity = @out output;
        select @out as the_output;
        """
        self.cursor.execute(sql, (con_id, iso, name))
        inserted_id: int = self.cursor.fetchall()
        self.cursor.commit()
        return inserted_id[0][0]

    def insert_case(self, case: Case):
        sql = "exec create_cases @country = ?, @date = ?, @total_cases = ?, @new_cases = ?, @total_deaths = ?, @new_deaths = ?, @reproduction_rate = ?;"
        self.cursor.execute(sql, case.to_list())
        self.cursor.commit()

    def insert_vaccines(self):
        pass

    def insert_tests(self):
        pass

    def commit(self):
        self.cursor.commit()
