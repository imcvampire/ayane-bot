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

    def latest_quote(self):
        self.db_cur.execute("SELECT * FROM quotes ORDER BY created_at DESC LIMIT(1);")
        return quote_info(self.db_cur.fetchone())

    def random_quote(self, author=None):
        if author == None:
            self.db_cur.execute("SELECT * FROM quotes ORDER BY random()")
        else:
            self.db_cur.execute("SELECT * FROM quotes WHERE author='%s' ORDER BY random()" % author)

        quote = self.db_cur.fetchone()
        if quote == None:
            return "Not found"
        else:
            return quote_info(quote)

    def list_quotes(self, author=None):
        if author == None:
            self.db_cur.execute("SELECT * FROM quotes ORDER BY created_at DESC;")
        else:
            self.db_cur.execute("SELECT * FROM quotes WHERE author='%s' ORDER BY created_at DESC" % author)

        quotes = self.db_cur.fetchall()
        if len(quotes) == 0:
            return "Not found"
        else:
            return map(quote_info, quotes)
