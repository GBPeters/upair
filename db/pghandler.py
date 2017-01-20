#__author__ = 'gijspeters'
"""
This module contains a PostgreSQL connection handler and require info.
"""

import psycopg2

DB_NAME='upair'
DB_HOST='localhost'
DB_USER='postgres'
DB_PASS='postgres'
DB_PORT='5432'
DB_DRIVER='org.postgresql.Driver'

class Connection:
    """
    Class handeling connection to a PostgreSQL database.
    """

    def __init__(self, autocommit=True, hardFail=False):
        self.autocommit = autocommit
        self.hardFail = hardFail
        self.__connect()

    def __enter__(self, autcommit=True, hardFail=False):
        self.__init__(autcommit, hardFail)
        return self

    def __exit__(self, type, value, traceback):
        try:
            self.close()
        except KeyboardInterrupt:
            raise
        except Exception:
            pass
        if isinstance(value, KeyboardInterrupt):
            return True
        else:
            return self.hardFail

    def __connect(self):
        self._connection = psycopg2.connect(database=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASS, port=DB_PORT)
        self._cursor = self._connection.cursor()
        self._copyfrom = self._cursor.copy_from

    def execute(self, sql):
        """
        Executes SQL code without return
        :param sql: The SQL to execute
        :return: None
        """
        self._cursor.execute(sql)
        if self.autocommit:
            self.commit()

    def selectOne(self, sql):
        """
        Executes SQL code with one return line
        :param sql: The sql to execute
        :return: A single tuple containing data
        """
        self._cursor.execute(sql)
        return self._cursor.fetchone()

    def selectAll(self, sql):
        """
        Executes SQL code with multiple return lines
        :param sql:  The sql to execute
        :return: All selected data
        """
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def commit(self):
        """
        Manual commit, if autocommit is off.
        :return: None
        """
        self._connection.commit()

    def close(self):
        """
        Close the connection. The Connection object becomes useless after close
        :return: None
        """
        self._connection.close()



