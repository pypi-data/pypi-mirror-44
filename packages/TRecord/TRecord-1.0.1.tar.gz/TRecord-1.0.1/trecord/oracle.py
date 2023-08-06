from trecord.database import Database
from trecord.error import TRecordError
import cx_Oracle


class CxOracle(Database):
    """This class implements the database using cx_Oracle"""
    def __init__(self) -> None:
        super().__init__()

    def connect(self, database_url: str):
        super().connect(database_url)
        if self.database_url.database:
            dsn = cx_Oracle.makedsn(self.database_url.host, self.database_url.port, self.database_url.database)
        else:
            dsn = self.database_url.host
        self.connection = cx_Oracle.connect(user=self.database_url.username,
                                            password=self.database_url.password,
                                            dsn=dsn,
                                            encoding="UTF-8",
                                            nencoding="UTF-8"
                                            )

    def query(self, query: str, limit: int = None):
        try:
            result = super().query(query, limit)
            return result
        except cx_Oracle.Error as err:
            raise TRecordError(err)

    def add_row_limit_in_query(self, query, limit):
        query = query.strip(' ;')
        if limit and query.lower().startswith('select'):
            return f'SELECT * FROM ({query}) WHERE ROWNUM <= {limit}'
        else:
            return query

    def get_data_type(self, type_code: int) -> str:
        """
        Check the type code and return a string description
        :param type_code:
        :return:
        """
        mapping = {
            cx_Oracle.STRING: 'STRING',
            cx_Oracle.BLOB: 'BLOB',
            cx_Oracle.BOOLEAN: 'BOOLEAN',
            cx_Oracle.CLOB: 'CLOB',
            cx_Oracle.DATETIME: 'DATETIME',
            cx_Oracle.FIXED_CHAR: 'FIXED_CHAR',
            cx_Oracle.FIXED_NCHAR: 'FIXED_NCHAR',
            cx_Oracle.INTERVAL: 'INTERVAL',
            cx_Oracle.NATIVE_INT: 'NATIVE_INT',
            cx_Oracle.NCHAR: 'NCHAR',
            cx_Oracle.NCLOB: 'NCLOB',
            cx_Oracle.ROWID: 'ROWID',
            cx_Oracle.BINARY: 'BINARY',
            cx_Oracle.NUMBER: 'NUMBER',
            cx_Oracle.TIMESTAMP: 'TIMESTAMP'
        }
        for key in mapping.keys():
            if type_code is key:
                return mapping[key]

        return str(type_code)

    def get_version(self) -> str:
        return '\n'.join(self.query('SELECT * FROM V$VERSION').get_col(0)) + '\n'

    def get_current_db(self) -> str:
        return ''

    def get_tables(self, database=None) -> list:
        if not database:
            database = self.database_url.username

        return self.query(f"SELECT table_name FROM ALL_TABLES WHERE owner = '{database.upper()}'").get_col(0)

    def get_ddl(self, table, database=None) -> str:
        if not database:
            database = self.database_url.username

        ddl = str(self.query(f"SELECT dbms_metadata.get_ddl('TABLE', '{table.upper()}', '{database.upper()}') FROM dual")[0][0]) + '\n;\n'

        for index in self.query(f"SELECT distinct index_name FROM all_ind_columns where table_name = '{table.upper()}' and table_owner = '{database.upper()}'").get_col(0):
            if f'"{index}"' in ddl:
                continue
            ddl = ddl + '\n' + str(self.query(f"SELECT dbms_metadata.get_ddl('INDEX', '{index}', '{database.upper()}') FROM dual")[0][0]) + '\n;\n'

        return ddl

if __name__ == '__main__':
    import sys

    sql = CxOracle()
    sql.connect(sys.argv[1])
    print(sql.get_version())
    print(sql.get_current_db())
    print(sql.get_tables('cs_orp'))
    print(sql.get_ddl('f_cs_request', 'cs_orp'))
