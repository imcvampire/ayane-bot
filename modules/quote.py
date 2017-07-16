def quote_info(q):
    return '[%s] "%s" - %s' % (q['id'], q['content'], q['author'])


class Quote:
    def __init__(self, db_conn, db_cur):
        self.db_conn = db_conn
        self.db_cur = db_cur


    def add_quote(self, author, content):
        self.db_cur.execute("INSERT INTO quotes (author, content, created_at) VALUES (%s, %s, CURRENT_TIME);",
                            (author, content))
        self.db_conn.commit()

    def get_latest_quote(self):
        self.db_cur.execute("SELECT * FROM quotes ORDER BY created_at DESC LIMIT(1);")
        return quote_info(self.db_cur.fetchone())

    def list_quotes(self):
        self.db_cur.execute("SELECT * FROM quotes ORDER BY created_at DESC;")
        quotes = self.db_cur.fetchall()
        return map(quote_info, quotes)
