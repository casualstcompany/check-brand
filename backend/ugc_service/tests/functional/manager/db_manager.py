import psycopg2


class ContextManagerDB:
    def __init__(self, dsn):
        self.conn = psycopg2.connect(dsn)
        self.cur = self.conn.cursor()

    def drop_schema_cascade(self, schema_name):
        try:
            self.cur.execute(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE")
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_all_by_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.cur.execute(file.read())
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
