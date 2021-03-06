import psycopg2
import psycopg2.extras
import config
import model.Labels


def get_connection(string):
    connection = psycopg2.connect(string)
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
        self.connection = get_connection(config.master_string)
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
    connection = get_connection(config.master_string)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    @staticmethod
    def select_matches_by_player(player_id, tournaments):
        if not tournaments:
            return []

        sql, param = in_clause([t['id'] for t in tournaments])
        CustomQueries.cursor.execute("""
select m.*
  from challo_match       m inner
  join challo_participant p on m.tournament_id = p.tournament_id and (m.player1_id = p.id or m.player2_id = p.id) inner
  join fg_player f          on f.id = p.player_id
 where f.id = %s and m.tournament_id in ({0})
        """.format(sql), [player_id, ] + param)
        return cursor_to_array(CustomQueries.cursor)

    @staticmethod
    def select_matches_by_players(player_urls, tournaments):
        p_sql, p_param = in_clause(player_urls)
        t_sql, t_param = in_clause([t['id'] for t in tournaments])
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
         and m.tournament_id in ({1})
        """.format(p_sql, t_sql), p_param + p_param + t_param)
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

    @staticmethod
    def select_match_count():
        CustomQueries.cursor.execute("select count(*) cnt from challo_match")
        val = cursor_to_array(CustomQueries.cursor)
        return val

    @staticmethod
    def select_tournamets_with_labels(labels: str) -> (list, list):
        if labels is None:
            return [], Table('fg_tournament').select_all()

        mls = model.Labels.labels_from_url(labels)
        sql = ' and '.join([m.where for m in mls if m.where])
        param = [m.param for m in mls if m.param]
        CustomQueries.cursor.execute("""
select * from fg_tournament
 where {0}
""".format(sql), param)
        return mls, cursor_to_array(CustomQueries.cursor)


class TranQueries:
    connection = get_connection(config.tran_string)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    @staticmethod
    def select_comments(url):
        TranQueries.cursor.execute("""
select * from comment where url = %s order by at
    """, (url,))
        return cursor_to_array(TranQueries.cursor)

    @staticmethod
    def insert_comment(url, text):
        TranQueries.cursor.execute("""
insert into comment (url, text, at) values(%s, %s, now())
        """, (url, text))

