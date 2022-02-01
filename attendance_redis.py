from pickle import NONE
import redis
import os 
import sys
import json
sys.path.insert(0, '/Users/Joen/Documents/COS-CM-BOT/secret')
import keys  

try:
    REDIS_URL = os.environ['REDIS_URL']
except:
    print("moving on to secrets")
    REDIS_URL = keys.REDIS_KEY

class RedisDB:

    def __init__(self, URL):
        self.r = redis.from_url(URL)

    def split_paths(self, path):
        dirs = path.split('/')
        main_key = dirs[0]
        subsequent_dirs = dirs[1:]
        return main_key, subsequent_dirs

    def get_value_from_path(self, path:str):
        main_key, subsequent_dirs = self.split_paths(path)
        r_return = self.r.get(main_key)
        if r_return != None:
            obj = json.loads(r_return)
            for this_dir in subsequent_dirs:
                try:
                    curr_group = obj[this_dir]
                except (TypeError, KeyError) as e:
                    return None
            return curr_group
        else:
            return None
    
#    def change_value_from_path(self, path:str, value:object):
#        main_key, subsequent_dirs = self.split_paths(path)
#        if len(subsequent_dirs) > 0:
#            obj = json.loads(self.r.get(main_key))
#            for this_dir in subsequent_dirs:
#                if type(obj) != str:
#                    try:
#                        obj = obj[this_dir]
#                        if this_dir == subsequent_dirs[-1]:
#                            obj = value
#                    except KeyError:
#                        break
#            self.r.set(main_key, json.dumps(obj))
#        else:
#            self.r.set(path, json.dumps(value))

#db = RedisDB(REDIS_URL)
#print(db.change_value_from_path("test/hello",[1,2,3]))
#print(db.get_value_from_path("test/hello"))

