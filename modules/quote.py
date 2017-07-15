
class Quote:
    def __init__(self, db_cur):
        self.db_cur = db_cur

        self.db_cur.execute("""CREATE TABLE IF NOT EXISTS quotes (
            id serial NOT NULL PRIMARY KEY,
            author varchar(25),
            content text
        );""")
        self.db_cur.execute("SELECT * FROM quotes;")
