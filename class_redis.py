import redis
import os 
import sys
import json
sys.path.insert(0, '/Users/Joen/Documents/COS-CM-BOT/secret')


try:
    print("using environment variables")
    REDIS_URL = os.environ['REDIS_URL']
except:
    import keys  
    print("moving on to redis secrets")
    REDIS_URL = keys.REDIS_KEY

#handles redis db, navigates and edits values
class RedisHandler:

    def __init__(self):
        self.r = redis.from_url(REDIS_URL)

    def split_paths(self, path):
        dirs = path.split('/')
        main_key = dirs[0]
        subsequent_dirs = dirs[1:]
        return main_key, subsequent_dirs

    # RECURSIVE NAVIGATION
    #----------------------
    #recursively navigates to object value via paths and edits value
    def add_value_from_path(self, paths:list, obj, value):
        if len(paths) > 1:
            new_obj = obj[paths[0]]
            paths.pop(0)
            self.two_change_path(paths, new_obj, value)
        elif len(paths) == 1:
            obj[paths[0]] = value
        return obj 

    #recursively navigates to object value via paths and returns value
    def navigate_to_value_from_path(self, paths:list, obj):
        if len(paths) > 1:
            new_obj = obj[paths[0]]
            paths.pop(0)
            self.two_change_path(paths, new_obj)
        elif len(paths) == 1:
            return obj[paths[0]]
    #----------------------
    
    #changes value at endpoint of paths
    def edit_value_from_path(self, paths:str, value):
        main_key, subsequent_dirs = self.split_paths(paths)        
        if len(subsequent_dirs) > 0:
            obj = json.loads(self.r.get(main_key))
            edited_obj = self.add_value_from_path(subsequent_dirs, obj, value)
            self.r.set(main_key, json.dumps(edited_obj))
        else:
            value_type = type(value)
            if value_type == str:
                self.r.set(main_key, value)
            else:
                self.r.set(main_key, json.dumps(value))

    #reads value at endpoint of paths
    def read_value_from_path(self, paths:str):
        main_key, subsequent_dirs = self.split_paths(paths)
        if len(subsequent_dirs) > 0:
            obj = json.loads(self.r.get(main_key))
            return self.navigate_to_value_from_path(subsequent_dirs, obj)
        else:
            return self.r.get(main_key)

#db = RedisHandler(REDIS_URL)
#print(db.edit_value_from_path("hello",0))
#print(db.read_value_from_path("hello/hi"))
#if __name__ == "__main__":
#    db = RedisHandler()
#    db.r.set("test_exp", "testing this", ex=60)
