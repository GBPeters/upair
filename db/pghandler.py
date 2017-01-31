#__author__ = 'gijspeters'
"""
This module contains a PostgreSQL connection handler and require info.
"""

import psycopg2

DB_DRIVER = 'org.postgresql.Driver'


class Config:
    """
    Configurations container
    """

    def __init__(self, name="upair", host="localhost", user="postgres", passw="postgres", port="5432"):
        self.DB_NAME = name
        self.DB_HOST = host
        self.DB_USER = user
        self.DB_PASS = passw
        self.DB_PORT = port


CONFIG = {
    "SERVER": Config(
        user="teammaja",
        passw="maja"
    ),
    "LOCAL": Config(
    )
}

class Connection:
    """
    Class handeling connection to a PostgreSQL database.
    """

    def __init__(self, conf="LOCAL", autocommit=True, hardFail=False):
        self.autocommit = autocommit
        self.hardFail = hardFail
        self.conf = CONFIG[conf]
        self.__connect()

    def __enter__(self):
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
        self._connection = psycopg2.connect(database=self.conf.DB_NAME, host=self.conf.DB_HOST, user=self.conf.DB_USER,
                                            password=self.conf.DB_PASS, port=self.conf.DB_PORT)
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



