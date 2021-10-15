#import sqlite3 as sql
import json 
import ast
import psycopg2 as sql
from private import HEROKU_URI
import csv


def create_inline_obj(mapped_val):
    emoji_list = {0:'Absent ❌',1:' Church ⛪️',2:'Zoom 👩🏻‍💻'}
    inline_array = []
    for key, value in mapped_val.items():
        inline_array.append([{'callback_data':f'attd_{key}', 'text':f'{key} | {emoji_list[value]}'}])
    inline_array.append([{'callback_data':'submit_attd', 'text':'Submit'}])
    return {'inline_keyboard':inline_array}

def update_name_mapped_val(data, mapped_val):
    data = data.replace("attd_","").replace("submit_attd","").replace("change_attd","")
    if mapped_val[data] < 2:
        mapped_val[data] += 1
    elif mapped_val[data] == 2:
        mapped_val[data] = 0
    return mapped_val

def init_name_mapped_val(class_id):
    return_dict = {}
    for name in get_all_names_for_class(class_id):
        return_dict[name] = 0
    return return_dict


def attd_insert_new_kid(name, attd_id):
    print("inserting kid")
    obj_state = get_attd_obj_by_id(attd_id)
    print(obj_state)
    if obj_state != False:
        print("inserting...")
        obj_state[name] = 1
        add_in_new_attd(attd_id, str(obj_state))

conn = sql.connect(HEROKU_URI, sslmode='require')

c = conn.cursor()
#
#c.execute("""CREATE TABLE users (
#           name text,
#           chat_id text,
#           session_id text,
#           session text,
#           class text,
#           admin boolean)
#""")
#
#def delete_entire_table(table_name):
#    with conn:
#        c.execute(f"DROP TABLE {table_name}")
#
#delete_entire_table("all_kids")
#c.execute("""CREATE TABLE all_kids (
#            name text,
#            session_code text,
#            age int,
#            session text,
#            class text
#)""")
#
#c.execute("""CREATE TABLE all_attd (
#            attd_id text,
#            attd_obj text
#)""")
#

#c.execute("INSERT INTO attendance VALUES('07102021', '1PP5','HELLO THERE')")

#c.execute("SELECT * FROM attendance")



def select_name_from_class(name, table_name):
    pass

def select_id_from_attd(id):
    pass

def get_all_from_column_table(col_name, table_name):
    pass

def add_in_new_attd(attd_id, attd_obj):
    with conn:
        get_all_distinct_ids = c.execute("SELECT DISTINCT attd_id FROM all_attd")
        get_all_distinct_ids = c.fetchall()
        if attd_id not in convert_fetchall_array(get_all_distinct_ids):    
            c.execute("""
            INSERT INTO all_attd VALUES (
                %(attd_id)s, 
                %(attd_obj)s
            )""",
            {"attd_id":attd_id, "attd_obj":attd_obj}
            )
        else:
            c.execute("""
            UPDATE all_attd 
            SET attd_obj = %(attd_obj)s
            WHERE attd_id = %(attd_id)s
            """,
            {"attd_id":attd_id, "attd_obj":attd_obj}
            )

def scrub(table_name):
    return ''.join( chr for chr in table_name if chr.isalnum() )

#deletes entire table

#DO NOT USE THIS IRL, ONLY USE IT TO DEBUGGG
def delete_values(table, variable, value):
    with conn:
        c.execute(f"""DELETE FROM {table} WHERE {variable} = '{value}'""",
        )

def get_attd_obj_by_id(attd_id):
    get_all_distinct_ids = c.execute("SELECT DISTINCT attd_id FROM all_attd")
    get_all_distinct_ids = c.fetchall()
    if attd_id in convert_fetchall_array(get_all_distinct_ids):
        return_obj_string = c.execute("SELECT attd_obj FROM all_attd WHERE attd_id = %(attd_id)s",
        {"attd_id":attd_id})
        return_obj_string = c.fetchone()[0]
        return ast.literal_eval(return_obj_string)
    else:
        return False

#class_id = FPP4
def get_all_names_for_class(class_id):
    c.execute("""
    SELECT name FROM all_kids WHERE session_code = %(class_id)s""",
    {"class_id":class_id}
    )
    return convert_fetchall_array(c.fetchall())

def insert_new_kid(obj):
    with conn:
        c.execute("""
        INSERT INTO all_kids VALUES (
            %(name)s,
            %(session_code)s,
            %(age)s,
            %(session)s,
            %(class)s
        )
        """,
        obj
        )
def startup_user(chat_id, user_name):    
    with conn:
        c.execute("""
        INSERT INTO users (name, chat_id) VALUES (%(user_name)s, %(chat_id)s )
        """,
        {"user_name":user_name,"chat_id":chat_id}
        )

def inside_bool_db(chat_id):
    get_all_distinct_ids = c.execute("SELECT DISTINCT chat_id FROM users")
    get_all_distinct_ids = c.fetchall()
    if str(chat_id) not in convert_fetchall_array(get_all_distinct_ids):
        return False
    else:
        return True

def insert_session_user(chat_id, session):
    with conn:
        c.execute("""UPDATE users 
            SET session = %(session)s
            WHERE chat_id = %(chat_id)s""",
            {"chat_id":chat_id, "session":session}
            )

def insert_class_user(chat_id, user_class):
    with conn:
        c.execute("""UPDATE users 
            SET class = %(user_class)s
            WHERE chat_id = %(chat_id)s""",
            {"chat_id":chat_id, "user_class":user_class})

def insert_session_id_user(chat_id, session_id):
    with conn:
        c.execute("""UPDATE users 
            SET session_id = %(session_id)s
            WHERE chat_id = %(chat_id)s""",
            {"chat_id":chat_id, "session_id":session_id})

def get_user_readable_data(chat_id): 
    get_read_tuple = c.execute("""
    SELECT name, session, class FROM users WHERE chat_id = %(chat_id)s
    """, 
    {"chat_id":str(chat_id)}
    )
    get_read_tuple = c.fetchone()
    return get_read_tuple[0], get_read_tuple[1], get_read_tuple[2]

def get_user_session_code(chat_id):
    get_all_distinct_ids = c.execute("SELECT DISTINCT chat_id FROM users")
    get_all_distinct_ids = c.fetchall()
    if chat_id in convert_fetchall_array(get_all_distinct_ids):
        get_read_tuple = c.execute("""
        SELECT session, class FROM users WHERE chat_id = %(chat_id)s
        """,
        {"chat_id":chat_id}
        )
        get_read_tuple = c.fetchone()
        return "".join(get_read_tuple)

def insert_full_user_data(obj):
    with conn:
        c.execute("""
        INSERT INTO users VALUES (
            %(name)s,
            %(chat_id)s,
            %(session)s,
            %(class)s
        )
        """,
        obj
        )  
#insert_full_user_data({"name":"test", "chat_id":"000000", "session":"fpp7", "class":"p7"})  
#create_attendance_table('lol')
#delete_entire_table("users")
#delete_entire_table("helloWorld")
#delete_entire_table("newtable")
#delete_values("all_attd","attd_id","FPP407102021")
def convert_fetchall_array(array):
    return [i[0] for i in array]
#add_in_new_attd("FPP407102021",'{"JOEN":1}')
#add_in_new_attd("FPP407102021",'{"mary":3,"daniel":1}')
#get_attd_obj_by_id("FPP407102021")
#add_in_new_attd("FPP407102021",'{"mary":1}')
#insert_new_kid({"name":"Daniel","session_code":"FPP4","age":12,"session":"FP","class":"P6"})
#insert_new_kid({"name":"John","session_code":"FPP4","age":12,"session":"FP","class":"P6"})
#insert_new_kid({"name":"Ian","session_code":"FPP4","age":12,"session":"FP","class":"P6"})
#insert_new_kid({"name":"Ron","session_code":"FPP4","age":12,"session":"FP","class":"P6"})
#print(get_all_names_for_class("FPP6"))
#insert_full_user_data({"name":"Joen Tan", "chat_id":"111111","session":"FP","class":"P5"})
#conn.commit()
#conn.close()
#print(get_user_session_code("111111"))
#
#def create_array_of_user_obj(csvname):
#    return_list = []
#    with open(csvname, 'r') as csvfile:
#        reader = csv.reader(csvfile, delimiter="\t")
#        for line in reader:
#            line = line[0].split(',')
#            print(line)
#            this_obj = {"name":line[3],"session_code":line[0]+line[1]+line[2],"age":00,"session":line[0]+line[1],"class":line[2]}
#            return_list.append(this_obj)
#    return return_list
#
#def add_all_kids_to_database(array):
#    for obj in array:
#        insert_new_kid(obj)
#
#add_all_kids_to_database(create_array_of_user_obj("CMALL.csv"))
#
#test_map_val = {'joen tan zhuo en':0,'chloe':1,'daniel':2,'hayley':0}

