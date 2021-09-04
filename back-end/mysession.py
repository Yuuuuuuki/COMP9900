from hashlib import sha1
import os
import time

create_session_id = lambda: sha1(bytes('%s%s' % (os.urandom(16), time.time()), encoding='utf-8')).hexdigest()

class Session:
    
    info_container = {
        # session_id: {'user': info}
    }

    def __init__(self, handler):
        self.handler = handler

        random_str = self.handler.get_cookie('session_id')
        if (not random_str) or (random_str not in self.info_container):
            random_str = create_session_id()
            self.info_container[random_str] = {}
        self.random_str = random_str

        self.handler.set_cookie('session_id', random_str, max_age=60)

    def __getitem__(self, item):
        return self.info_container[self.random_str].get(item)

    def __setitem__(self, key, value):
        self.info_container[self.random_str][key] = value

    def __delitem__(self, key):
        if self.info_container[self.random_str].get(key):
            del self.info_container[self.random_str][key]

    def delete(self):
        del self.info_container[self.random_str]

