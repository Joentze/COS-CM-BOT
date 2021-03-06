from attendance_handler import create_inline_obj
from class_redis import RedisHandler
from class_pg import PostgresHandler
import json 

class AttendanceHandler:
    
    def __init__(self):
        self.red = RedisHandler()
        self.pg = PostgresHandler()

    #gets attendance for sunday
    def get_attendance(self, attd_id):
        if self.red.r.exists(attd_id):
            obj = self.red.r.get(attd_id)
            return self.create_inline_object(json.loads(obj))
        else:
            return self.create_inline_object(json.loads(self.add_attendance(attd_id)))

    #adds attendance for sunday
    def add_attendance(self, attd_id):
        session_code = attd_id[:4]
        names = self.pg.get_names_in_class(session_code)
        obj = {}
        for name in names:
            obj[name] = 0
        self.red.r.set(attd_id, json.dumps(obj))
        return obj

    def create_inline_object(self, obj):
        emoji_list = {0:'Absent ❌',1:' Church ⛪️',2:'Zoom 👩🏻‍💻'}
        inline_array = []
        for k, v in obj.items():
            inline_array.append([{'callback_data':f'attd_{k.strip()}', 'text':f'{k} | {emoji_list[v]}'}])
        inline_array.append([{'callback_data':'submit_attd', 'text':'Submit'}])
        return {'inline_keyboard':inline_array}

    #---- WHEN NAME KEY IS PRESSED ----
    #updates attendance in redis and returns object for inline keyboard
    def update_attendance_name(self, name, attd_id):
        curr_obj = json.loads(self.red.r.get(attd_id))
        if curr_obj[name] < 2:
            curr_obj[name] += 1
        elif curr_obj[name] == 0:
            curr_obj[name] = 0
        self.red.r.set(attd_id, json.dumps(curr_obj))
        return self.create_inline_object(curr_obj)

    #adds name of kid to attendance
    def add_kid(self, name, attd_id):
        session_code = attd_id[:4]
        names = self.pg.get_names_in_class(session_code)
        if name not in names:
            self.pg.add_kid(name, session_code)
            if self.red.r.exists(attd_id):
                self.red.edit_value_from_path(f"{attd_id}/{name}", 1)
            else:
                self.add_attendance(attd_id)    
            return True
        else:
            return None

    #udpates absentee cnt table
    def update_absentee_cnt(self, attd_id):
        absent_id = f"absentee_{attd_id[:4]}_{attd_id[-4:]}"
        attd_obj = json.loads(self.red.r.get(attd_id))
        updated_names = self.pg.updated_names(attd_id[:4], attd_id[-8:])
        for k, v in attd_obj.items():
            if v == 0:
                if k not in updated_names:
                    attd_obj[k] += 1
            elif v > 0:
                attd_obj[k] = 0
        self.red.r.set(absent_id, json.dumps(attd_obj))
        self.pg.update_date(attd_id[:4], attd_id[-8:])

if __name__ == "__main__":
    test = AttendanceHandler()
    test.add_attendance("FPP6test")
    test.update_absentee_cnt("FPP6test")

