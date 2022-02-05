import psycopg2
import os 
import sys
sys.path.insert(0, '/Users/Joen/Documents/COS-CM-BOT/secret')

try:
    print("using environment variables")
    HEROKU_CRED = os.environ["HEROKU_POSTGRES_CREDENTIALS"]
except:
    import keys  
    print("moving on to secrets")
    HEROKU_CRED = keys.PG_HEROKU_KEY

class PostgresHandler:
    def __init__(self):
        self.conn = psycopg2.connect(HEROKU_CRED, sslmode="require")
        self.c = self.conn.cursor()

    #adds kid into all_kids table
    def add_kid(self, name, session_code): 
        with self.conn:
            self.c.execute("""
            INSERT INTO all_kids
            (
                %(name)s,
                %(session_code)s,
                %(session)s,
                %(class)s,
                0
            )
            """,
            {
                "name":name,
                "session_code":session_code,
                "session":session_code[:2],
                "class":session_code[-2:],
            }
            )
    #remove from kid from all_kids table
    def remove_kid(self, name, session_code): 
        with self.conn:
            self.c.execute("""
            DELETE FROM all_kids 
            WHERE name = %(name)s
            AND
            session_code = %(session_code)s
            """,
            {
                "name":name,
                "session_code":session_code,
            }
            )

    def get_names_in_class(self, session_code):
        self.c.execute("""
        SELECT name FROM all_kids
        WHERE session_code = %(session_code)s
        """,
        {
            "session_code":session_code
        }
        )
        return [i[0] for i in self.c.fetchall()]

    def get_chat_ids(self):
        self.c.execute(
        """
        SELECT chat_id FROM users
        """
        )
        return [i[0] for i in self.c.fetchall()]
    

    def updated_names(self, session_code, date):
        self.c.execute(
        """
        SELECT name FROM all_kids
        WHERE session_code = %(session_code)s 
        AND
        date = %(date)s
        """,
        {
            "session_code":session_code,
            "date":date
        }
        )
        return [i[0] for i in self.c.fetchall()]
    
    def update_date(self, session_code, date):
        with self.conn:
            self.c.execute(
                """
                UPDATE all_kids
                SET date = %(date)s
                WHERE session_code = %(session_code)s
                """,
                {
                    "date":date,
                    "session_code":session_code
                }
                )
        
if __name__ == "__main__":
    pg =  PostgresHandler()
    with pg.conn:
        pg.c.execute("ALTER TABLE all_kids DROP COLUMN absentee_")
