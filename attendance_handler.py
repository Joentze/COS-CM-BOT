#import sqlite3 as sql
from datetime import date, timedelta
import json 
import ast
#from private import HEROKU_URI
import csv
import psycopg2 as sql
import msg as message
import os
import sys
sys.path.insert(0, '/Users/Joen/Documents/COS-CM-BOT/secret')


try:
    print("using environment variables")
    HEROKU_CRED = os.environ["HEROKU_POSTGRES_CREDENTIALS"]
except:
    import secret.keys as keys
    print("moving on to secrets")
    HEROKU_CRED = keys.PG_HEROKU_KEY


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

def update_absentee_cnt(date, data, session_code, curr_cnt):
    #curr_cnt = mapped_val[data]
    if curr_cnt==0:
        c.execute("""SELECT absentee_cnt FROM all_kids
                    WHERE name = %(name)s AND session_code = %(session_code)s""",
                    {"name":data, "session_code":session_code})
        set_cnt = c.fetchone()[0]
        with conn:
            if add_last_update(data, session_code, date):
                c.execute(
                    """
                    UPDATE all_kids
                    SET absentee_cnt = %(set_cnt)s
                    WHERE name = %(name)s AND session_code = %(session_code)s
                    """,
                    {"name":data, "session_code":session_code, "set_cnt":set_cnt+1}
                )
    elif curr_cnt > 0:
        with conn:
            c.execute(
                """
                UPDATE all_kids
                SET absentee_cnt = 0
                WHERE name = %(name)s AND session_code = %(session_code)s
                """,
                {"name":data, "session_code":session_code}
            )

#updates last update column in ddmmyyyy format in string
def add_last_update(data, session_code, date):
    
    c.execute("""
    SELECT last_update FROM all_kids
    WHERE name = %(name)s AND session_code = %(session_code)s
    """,
    {"name":data, "session_code":session_code})
    get_last_update_date = c.fetchone()[0]
    if get_last_update_date == date:
        print("date is updated")
        return False
    else:
        print("date is not updated")
        c.execute("""
        UPDATE all_kids
        SET last_update = %(last_update)s
        WHERE name = %(name)s AND session_code = %(session_code)s
        """,
        {"name":data, "session_code":session_code, "last_update":date})
        return True

def get_names_absentee_cnt(session_code):
    with conn:
        c.execute("""
        SELECT name, absentee_cnt
        FROM all_kids
        WHERE session_code = %(session_code)s AND absentee_cnt > 2
        """,
        {"session_code":session_code}
        )
        return_set = []
        for name, cnt in c.fetchall():
            this_line = f"{name}: 🚩 X {cnt}"
            return_set.append(this_line)
        return '\n'.join(return_set)


def collate_absentee_cnt(date, session_code, mapped_val):
    for name, attendance_state in mapped_val.items():
        print(f'updating {name}')
        update_absentee_cnt(date, name, session_code, attendance_state)

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

conn = sql.connect(HEROKU_CRED, sslmode='require')


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
            this_obj = {"name":line[3].strip(),"session_code":line[0]+line[1]+line[2],"session":line[0]+line[1],"class":line[2]}
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

descending_class_conversion_map = {
    "P6":"TC",
    "P5":"P6",
    "P4":"P5",
    "P3":"P4",
    "P2":"P3",
    "P1":"P2",
    "K2":"P1",
    "K1":"K2",
    "N1":"K1",
    "N0":"N1",
}

undo_class_conversion_map ={
    "TC":"P6",
    "P6":"P5",
    "P5":"P4",
    "P4":"P3",
    "P3":"P2",
    "P2":"P1",
    "P1":"K2",
    "K2":"K1",
    "K1":"N1",
    "N1":"N0",
}

def update_all_kids_classes(conversion_map, all_session_codes):
    for class_now, class_next in conversion_map.items():
        with conn:
            print(f'replaced {class_now}')
            c.execute("""
            UPDATE all_kids SET class = %(class_next)s WHERE class = %(class_now)s""",
            {"class_now":class_now, "class_next":class_next}
            )
    for session_code in all_session_codes:
        with conn:
            print(f'updating session code: {session_code}')
            c.execute("""
                UPDATE all_kids
                SET session_code = %(session_code_next)s
                WHERE session_code = %(session_code_now)s
            """,
            {"session_code_next":session_code[0:2]+conversion_map[session_code[-2:]], "session_code_now":session_code})
    
#RESETS ALL CLASS

def change_class_from_session_code(all_session_codes):
    for session_code in all_session_codes:
        print(session_code)
        with conn:
            print(session_code[-2:])
            c.execute("""
            UPDATE all_kids
            SET class = %(class)s
            WHERE session_code = %(session_code)s
            """,{
                "session_code":session_code,
                "class":session_code[-2:]
            })

def get_all_chat_id():
    c.execute("SELECT chat_id FROM users")
    get_all_names_chat_id = c.fetchall()
    return get_all_names_chat_id


def delete_user_from_attd(chat_id):
    with conn:
        c.execute("""
        DELETE FROM users 
        WHERE chat_id = %(chat_id)s
        """, 
        {"chat_id":str(chat_id)}
        )

def write_raw_sql(query_string):
    with conn:
        c.execute(query_string)


if __name__ == "__main__":
    #update_all_kids_classes(descending_class_conversion_map, message.all_session_codes)
    #update_all_kids_classes(conversion_map)
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
    #update_all_kids_classes(descending_conversion_map)
    #change_class_from_session_code(message.all_session_codes)

    #print(write_raw_sql("""SELECT * FROM all_attd WHERE attd_id LIKE '________2021'"""))
    #update_absentee_cnt("25122021","Levi Ow Yong", "FTN0",2)
    pass
