import psycopg2
import psycopg2.extras
import config


def get_connection():
    connection = psycopg2.connect(config.connection_string)
    connection.autocommit = True
    return connection


def cursor_to_array(cursor):
    ret = []
    for row in cursor:
        ret.append({i: row[i] for i in cursor.index})
    return ret


def in_clause(array):
    array = list(set(array))
    return ', '.join(['%s' for _ in array]), array


class Table:
    def __init__(self, table_name):
        self.connection = get_connection()
        self.table_name = table_name
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def select_one(self, where, params):
        return self.select(where, params)[0]

    def select_all(self):
        self.cursor.execute("SELECT * FROM {0}".format(self.table_name))
        return cursor_to_array(self.cursor)

    def select(self, where, params):
        self.cursor.execute("SELECT * FROM {0} WHERE {1}".format(self.table_name, where), params)
        return cursor_to_array(self.cursor)

    def select_in(self, key, array):
        if array is None or len(array) == 0:
            return []
        sql, param = in_clause(array)
        self.cursor.execute("SELECT * FROM {0} WHERE {1} IN ({2})".format(self.table_name, key, sql), param)
        return cursor_to_array(self.cursor)

    def delete_all(self):
        self.cursor.execute("DELETE FROM {0}".format(self.table_name))

    def delete(self, where, params):
        self.cursor.execute("DELETE FROM {0} WHERE {1}".format(self.table_name, where), params)

    def insert_with_array(self, values):
        self.cursor.execute("INSERT INTO {0} VALUES ({1})".format(
            self.table_name, ", ".join(['%s' for _ in values])), values
        )

    def insert_with_dictionary(self, dic):
        columns = ', '.join(dic.keys())
        places = ', '.join(['%s' for _ in dic.values()])
        values = [v for v in dic.values()]
        self.cursor.execute(
            "INSERT INTO {0} ({1}) VALUES ({2})".format(self.table_name, columns, places), values
        )

    def update_with_tournament_id(self, tournament_id, row_id, values):
        self.cursor.execute("UPDATE {0} SET {1} WHERE tournament_id = %s AND id = %s".format(
            self.table_name, ", ".join(['{0} = %s'.format(v[0]) for v in values])
        ), [v[1] for v in values] + [tournament_id, row_id])

    def update(self, row_id, values):
        self.cursor.execute("UPDATE {0} SET {1} WHERE id = %s".format(
            self.table_name, ", ".join(['{0} = %s'.format(v[0]) for v in values])
        ), [v[1] for v in values] + [row_id])

    def update_all(self, values):
        self.cursor.execute("UPDATE {0} SET {1}".format(
            self.table_name, ", ".join(['{0} = %s'.format(v[0]) for v in values])
        ), [v[1] for v in values])


class CustomQueries:
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    @staticmethod
    def select_matches_by_player(player_id):
        CustomQueries.cursor.execute("""
select m.*
  from challo_match       m inner
  join challo_participant p on m.tournament_id = p.tournament_id and (m.player1_id = p.id or m.player2_id = p.id) inner
  join fg_player f          on f.id = p.player_id
 where f.id = %s
        """, (player_id,))
        return cursor_to_array(CustomQueries.cursor)

    @staticmethod
    def select_matches_by_players(player_urls):
        sql, param = in_clause(player_urls)
        CustomQueries.cursor.execute("""
select m.*
        from challo_match       m
  inner join challo_participant p1
          on m.tournament_id = p1.tournament_id and m.player1_id = p1.id
  inner join challo_participant p2
          on m.tournament_id = p2.tournament_id and m.player2_id = p2.id
  inner join fg_player f1 on f1.id = p1.player_id
  inner join fg_player f2 on f2.id = p2.player_id
       where f1.url in ({0}) and f2.url in ({0})
        """.format(sql), param + param)
        return cursor_to_array(CustomQueries.cursor)

    @staticmethod
    def select_participants_by_players(player_urls):
        sql, param = in_clause(player_urls)
        CustomQueries.cursor.execute("""
select p.*
        from challo_participant p
  inner join fg_player f
          on f.id = p.player_id
       where f.url in ({0})
        """.format(sql), param)
        return cursor_to_array(CustomQueries.cursor)
