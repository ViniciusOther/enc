import json
import os

class config:
    #region keys
    API_ID = 
    API_HASH = ""
    #endregion
    PARENT_CHAT_ID = ""
    ALLOW_URLS = False

    def add_source(self, id):
        pass

    def add_destination(self, id):
        pass

    def add_relation(self, s, t):
        json = self.read_json()
        if s in json:
            json[s].append(t)
        else:
            json[s] = [t]
        self.write_json("relations.json", json)

    def write_json(self, fn, j):
        try:
            with open(fn, 'w') as f:
                json.dump(j, f, indent=1)
            return True
        except:
            return False

    def read_json(self):
        with open('relations.json', 'r') as f:
            j = json.load(f)
            return j
        return None


