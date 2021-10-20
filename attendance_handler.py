#import sqlite3 as sql
from datetime import date, timedelta
import json 
import ast
import psycopg2 as sql
from private import HEROKU_URI
import csv


def create_inline_obj(mapped_val):
    emoji_list = {0:'Absent ❌',1:' Church ⛪️',2:'Zoom 👩🏻‍💻'}
    inline_array = []
    for key, value in mapped_val.items():
        inline_array.append([{'callback_data':f'attd_{key.strip()}', 'text':f'{key} | {emoji_list[value]}'}])
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
        return_dict[name.strip()] = 0
    return return_dict


def attd_insert_new_kid(name, attd_id):
    print("inserting kid")
    obj_state = get_attd_obj_by_id(attd_id)
    print(obj_state)
    if obj_state != False:
        print("inserting...")
        obj_state[name.strip()] = 1
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
def delete_entire_table(table_name):
    with conn:
        c.execute(f"DROP TABLE {table_name}")
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

def get_attd_with_substring(sub_string):
    c.execute("""
        SELECT * FROM all_attd WHERE attd_id LIKE %(sub_string)s
    """,
    {"sub_string":f'{sub_string}'}
    )
    #PUTS ALL ATTENDANCE OBJ IN ARRAY
    return [ast.literal_eval(i[1]) for i in c.fetchall()]

def convert_fetchall_array(array):
    return [i[0] for i in array]

def create_array_of_user_obj(csvname):
    return_list = []
    with open(csvname, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for line in reader:
            line = line[0].split(',')
            print(line)
            this_obj = {"name":line[3].strip(),"session_code":line[0]+line[1]+line[2],"age":00,"session":line[0]+line[1],"class":line[2]}
            return_list.append(this_obj)
    return return_list


def count_total_in_attd_substr(array_attendance):
    count = 0
    for this_dict in array_attendance:
        all_values = list(this_dict.values())
        for value in all_values:
            if value > 0:
                count+=1
            else:
                pass
    return count

def add_all_kids_to_database(array):
    for obj in array:
        insert_new_kid(obj)

def get_attd_count(input_string):
    if len(input_string) == 12:
        all_attd = get_attd_with_substring(input_string)
        get_total_number_for_session = count_total_in_attd_substr(all_attd)
        return get_total_number_for_session
    else:
        return False

def allsundays(year):
    year = int(year)
    d = date(year, 1, 1)                    # January 1st
    d += timedelta(days = 6 - d.weekday())  # First Sunday
    while d.year == year:
        yield d
        d += timedelta(days = 7)

def all_sunday_object(sundays):
    return_dict = {}
    for this_sun in sundays:
        this_sun = this_sun.strftime("%d%m%Y")
        get_month = this_sun[2:4]#this_sun.split("/")[1]
        if get_month not in list(return_dict.keys()):
            return_dict[get_month] = [this_sun]
        else:
            return_dict[get_month].append(this_sun)
    return return_dict

#month in numbers
def get_attd_id_combis(month, year):
    return_dict = {}
    all_sun = allsundays(year)
    all_sun_obj = all_sunday_object(all_sun)
    get_all_weeks = all_sun_obj[month]
    all_session = ["FJ","SJ","FT","FP","SP","ST"]
    for session in all_session:
        return_dict[session] = [f"{session}__{week}" for week in get_all_weeks]
    return return_dict

#age_group accepts P or J 
def get_age_group_total_obj(age_group ,attd_id_date_obj):
    if age_group == "P" or age_group == "J" or age_group == "T":
        return_list = []
        s_one = F"S{age_group}"
        f_one = F"F{age_group}"
        sp_date = attd_id_date_obj[s_one]
        fp_date = attd_id_date_obj[f_one]
        len_of_date = len(fp_date)
        #counts for five weeks
        for week in range(0,5):
            if week < len_of_date:
                sum_sp = get_attd_count(sp_date[week])
                sum_fp = get_attd_count(fp_date[week])
                return_list.append({f_one:sum_fp, s_one:sum_sp})
            else:
                return_list.append({f_one:0, s_one:0})
        return return_list
    else:
        return False

def get_praise_jam_attendance_array(month, year):
    date_obj = get_attd_id_combis(month,year)
    jam_age_group = get_age_group_total_obj("J", date_obj)
    praise_age_group = get_age_group_total_obj("P", date_obj)
    tots_age_group = get_age_group_total_obj("T", date_obj)
    return {"P":praise_age_group, "J":jam_age_group, "T":tots_age_group}

if __name__ == "__main__":
    #print(get_attd_count_month("FP","102021"))
    #date_obj = get_attd_id_combis("10","2021")
    #print(get_age_group_total_obj("P", date_obj))
    #print(all_sunday_object(allsundays(2021)))
    #add_all_kids_to_database(create_array_of_user_obj("CMALL.csv"))
    #delete_entire_table("all_kids")
    #print(get_praise_jam_attendance_array("10","2021"))
    #
    #with conn:
    #    c.execute("UPDATE all_kids SET session")
    #
    pass