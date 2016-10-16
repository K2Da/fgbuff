import psycopg2
import psycopg2.extras
import config


def get_connection():
    connection = psycopg2.connect(config.connection_string)
    connection.autocommit = True
    return connection


class Table:
    def __init__(self, table_name):
        self.connection = get_connection()
        self.table_name = table_name
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def select_one(self, where, params):
        return self.select(where, params)[0]

    def _cursor_to_array(self):
        ret = []
        for row in self.cursor:
            ret.append({i: row[i] for i in self.cursor.index})
        return ret

    def select_all(self):
        self.cursor.execute("SELECT * FROM {0}".format(self.table_name))
        return self._cursor_to_array()

    def select(self, where, params):
        self.cursor.execute("SELECT * FROM {0} WHERE {1}".format(self.table_name, where), params)
        return self._cursor_to_array()

    def select_in(self, key, array):
        if array is None or len(array) == 0:
            return []
        sql, param = self._in_clause(array)
        self.cursor.execute("SELECT * FROM {0} WHERE {1} IN ({2})".format(self.table_name, key, sql), param)
        return self._cursor_to_array()

    def delete_all(self):
        self.cursor.execute("DELETE FROM {0}".format(self.table_name))

    def delete(self, where, params):
        self.cursor.execute("DELETE FROM {0} WHERE {1}".format(self.table_name, where), params)

    def insert(self, values):
        self.cursor.execute("INSERT INTO {0} VALUES ({1})".format(
            self.table_name, ", ".join(['%s' for _ in values])), values
        )

    def update(self, row_id, values):
        self.cursor.execute("UPDATE {0} SET {1} WHERE id = %s".format(
            self.table_name, ", ".join(['{0} = %s'.format(v[0]) for v in values])
        ), [v[1] for v in values] + [row_id])

    @staticmethod
    def _in_clause(array):
        array = list(set(array))
        return ', '.join(['%s' for _ in array]), array


