import json

from FileHelper import *


class DataManager:
    def __init__(self):
        self.watch_list = []

        self.f = FileHelper("sources.json")
        if self.f.exists():
            sources = json.loads(self.f.read())
            self.watch_list = sources["sources"]
        else:
            self.f.write("{}")

    def add_source(self, source):
        if source not in self.watch_list:
            self.watch_list.append(source)
            sources = json.loads(self.f.read())
            sources["sources"] = self.watch_list
            js = json.dumps(sources)
            self.f.overwrite(js)
        return self

    def update(self):
        df = FileHelper("data.json")
        pre = json.loads(df.read())
        data = {}
        for source in self.watch_list:
            fs = FileHelper(source)
            tracks = json.loads(fs.read())
            for id in tracks:
                data[source.strip(".json")+":"+id] = tracks[id]
        data.update(pre)
        js = json.dumps(data)
        df.overwrite(js)




