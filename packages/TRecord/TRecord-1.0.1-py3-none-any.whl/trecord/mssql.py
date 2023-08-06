from trecord.database import Database
from trecord.error import TRecordError
import pyodbc
import re
from datetime import datetime, date


class PyODBCMSSQL(Database):
    """This class implements the database using PyMySQL"""

    def __init__(self) -> None:
        super().__init__()

    def connect(self, database_url: str):
        super().connect(database_url)
        self.connection = pyodbc.connect(
            f'DSN={self.database_url.host};UID={self.database_url.username};PWD={self.database_url.password}'
        )
        if self.database_url.database:
            self.write("USE {}".format(self.database_url.database))

    def query(self, query: str, limit: int = None):
        try:
            result = super().query(query, limit)
            return result
        except pyodbc.Error as err:
            raise TRecordError(err)

    def add_row_limit_in_query(self, query, limit):
        if limit and not re.search(r'\s+top\s+', query, re.IGNORECASE):
            query = re.sub(r'^select\s+', 'select top {} '.format(limit), query)
        return query

    def get_data_type(self, type_code: int) -> str:
        """
        Check the type code and return a string description
        :param type_code:
        :return:
        """
        mapping = {
            pyodbc.STRING: 'STRING',
            pyodbc.BINARY: 'BINARY',
            pyodbc.NUMBER: 'NUMBER',
            pyodbc.Date: 'DATE',
            pyodbc.Time: 'TIME',
            pyodbc.Timestamp: 'TIMESTAMP',
            int: 'INTEGER',
            bool: 'BOOLEAN',
            datetime: 'DATETIME',
            date: 'DATE'
        }
        for key in mapping.keys():
            if type_code is key:
                return mapping[key]

        return str(type_code)

    def get_version(self) -> str:
        return self.query('SELECT @@VERSION')[0][0]

    def get_current_db(self) -> str:
        return self.query('SELECT DB_NAME()')[0][0]

    def get_tables(self, database=None) -> list:
        if not database:
            database = self.get_current_db()
        return list(
            self.query("select table_name "
                       "from {}.information_schema.tables;".format(database)).get_col(0)
        )

    def get_ddl(self, table, database=None):
        if not database:
            database = self.get_current_db()

        # set the database context
        ddl = f'USE {database};\n\n'

        # column definitions
        column_data = self.query(
            "SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, "
            "NUMERIC_PRECISION, NUMERIC_SCALE, DATETIME_PRECISION, IS_NULLABLE FROM {}.INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_NAME = '{}' ORDER BY ORDINAL_POSITION;".format(database, table))

        if not column_data.height:
            return ''

        full_table_name = column_data[0][1] + '.' + column_data[0][2]
        ddl += f'CREATE TABLE {full_table_name}\n(\n'
        for column in column_data.dict:
            # 'DATA_TYPE(STRING)' -> 'DATA_TYPE'
            column = {re.sub(r'\(.*\)', '', key): column[key] for key in column.keys()}

            column_name = column['COLUMN_NAME']
            if 'char' in column['DATA_TYPE']:
                column_type = f"{column['DATA_TYPE'].upper()}({column['CHARACTER_MAXIMUM_LENGTH']})"
            else:
                column_type = column['DATA_TYPE'].upper()

            if column['IS_NULLABLE'] == 'NO':
                column_null = 'NOT NULL'
            else:
                column_null = 'NULL'

            ddl += f'\t{column_name} {column_type} {column_null},\n'
        ddl += ')\n;\n\n'

        # constraints
        constraints_query = """SELECT
            CONSTRAINT_NAME, ORDINAL_POSITION, TABLE_NAME, COLUMN_NAME, IS_UNIQUE, IS_PRIMARY_KEY
            FROM {}.INFORMATION_SCHEMA.KEY_COLUMN_USAGE k
            JOIN SYS.INDEXES i
            ON   k.constraint_name = i.name
            WHERE table_name = '{}'
            ORDER BY constraint_name, ordinal_position
            """.format(database, table)
        constraints = self.query(constraints_query)

        def get_constraint_ddl(constraint_name, constraint_columns, constraint_pk, constraint_unique):
            constraint_ddl = ''
            if constraint_name:  # Wrap up for last constraint
                constraint_ddl = f'ALTER TABLE {full_table_name} ADD CONSTRAINT {constraint_name} '
                if constraint_pk:
                    constraint_ddl += f'PRIMARY KEY ({", ".join(constraint_columns)});\n'
                elif constraint_unique:
                    constraint_ddl += f'UNIQUE ({", ".join(constraint_columns)});\n'

            return constraint_ddl

        if not constraints.height:
            ddl += '-- No Constraints Found!\n'
        else:
            constraint_name = None
            constraint_columns = []
            constraint_pk = False
            constraint_unique = False
            for r in constraints:
                if constraint_name != r[0]:  # A new constraint found
                    ddl += get_constraint_ddl(constraint_name, constraint_columns, constraint_pk, constraint_unique)

                    # set for the new constraint
                    constraint_name = r[0]
                    constraint_columns = [r[3]]
                    constraint_pk = r[5]
                    constraint_unique = r[4]
                else:
                    constraint_columns.append(r[3])

            ddl += get_constraint_ddl(constraint_name, constraint_columns, constraint_pk, constraint_unique)

        return ddl


if __name__ == '__main__':
    import sys

    sql = PyODBCMSSQL()
    sql.connect(sys.argv[1])
    print(sql.get_version())
    print(sql.get_current_db())
    print(sql.get_ddl('vw_eBay_NiceLinksForSurvey'))
    print(sql.get_ddl('tblREScorecardRule'))
