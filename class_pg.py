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
    
    def get_absentees_from_class(self, session_code):
        self.c.execute(
            """
            SELECT name, absentee_cnt FROM all_kids
            WHERE absentee_cnt > 3 AND
            session_code = %(session_code)s
            """,
            {
                "session_code":session_code
            }
        )
        return self.c.fetchall()
    
    def return_updated(self, session_code, date):
        self.c.execute(
        """
        SELECT name FROM all_kids
        WHERE session_code = %(session_code)s 
        AND
        last_update = %(date)s
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
                SET last_update = %(date)s
                WHERE session_code = %(session_code)s
                """,
                {
                    "date":date,
                    "session_code":session_code
                }
                )
    def startup_user(self, chat_id, user_name):    
        with self.conn:
            self.c.execute(
                """
                INSERT INTO users 
                (name, chat_id) 
                VALUES (%(user_name)s, %(chat_id)s)
                """,
                {"user_name":user_name,"chat_id":chat_id}
                )

    def delete_user(self, chat_id):
        with self.comm:
            self.c.execute (
                """
                DELETE FROM users
                WHERE chat_id = %(chat_id)s
                """,
                {
                    "chat_id":chat_id,
                }
            )
    def get_session_id(self, chat_id):
        self.c.execute(
        """
        SELECT session_id 
        FROM users
        WHERE chat_id = %(chat_id)s
        """,
        {
            "chat_id":chat_id
        }
        )
        return self.c.fetchone()[0]

    def get_user_data(self, chat_id): 
        get_read_tuple = self.c.execute(
        """
        SELECT name, session, class
        FROM 
        users WHERE chat_id = %(chat_id)s
        """, 
        {
            "chat_id":str(chat_id)
        }
        )
        get_read_tuple = self.c.fetchone()
        return get_read_tuple[0], get_read_tuple[1], get_read_tuple[2]

        
if __name__ == "__main__":
    pg =  PostgresHandler()
