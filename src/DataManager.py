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
            source_data = {}
            fs = FileHelper(source)
            if not fs.exists():
                self.watch_list.remove(source)
                continue
            tracks = json.loads(fs.read())
            source_name = source.replace(".json", "")
            for id in tracks:
                source_data[source_name+":"+id] = tracks[id]
            source_data = dict(sorted(source_data.items(), key=lambda x: x[1]['name'].lower()))
            data.update(source_data)
        data_id = []
        for id in data:
            data_id.append(id)
        delete_queue = []
        for id in pre:
            if id not in data_id:
                delete_queue.append(id)
        for id in delete_queue:
            pre.pop(id)
        data.update(pre)
        js = json.dumps(data)
        df.overwrite(js)

        sources = json.loads(self.f.read())
        sources["sources"] = self.watch_list
        js = json.dumps(sources)
        self.f.overwrite(js)




