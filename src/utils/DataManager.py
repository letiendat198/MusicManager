import json
import os

from src.utils.FileHelper import FileHelper


class DataManager:
    def __init__(self):
        self.watch_list = []

        self.f = FileHelper("../sources.json")
        if self.f.exists():
            sources = json.loads(self.f.read())
            self.watch_list = sources["sources"]
        else:
            sources = {}
            sources["sources"] = ""
            js = json.dumps(sources)
            self.f.overwrite(js)

    def add_source(self, source):
        if source not in self.watch_list:
            self.watch_list.append(source)
            sources = json.loads(self.f.read())
            sources["sources"] = self.watch_list
            js = json.dumps(sources)
            self.f.overwrite(js)
        return self

    def update(self):
        df = FileHelper("../data.json")
        if not df.exists():
            df.write("{}")
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
            # if "download-path" in pre[id]:
            #     p = pre[id]["download-path"]
            #     pf = FileHelper(p)
            #     if pf.exists():
            #         pf.delete()
            pre.pop(id)
        data.update(pre)
        js = json.dumps(data)
        df.overwrite(js)

        sources = json.loads(self.f.read())
        sources["sources"] = self.watch_list
        js = json.dumps(sources)
        self.f.overwrite(js)
        return self

    def validate_download(self):
        df = FileHelper("../data.json")
        if not df.exists():
            df.write("{}")
        tracks = json.loads(df.read())
        print("Validating", len(tracks), "entries")
        count = 0
        for track in tracks:
            if "download-path" in tracks[track]:
                count += 1
                path = tracks[track]["download-path"]
                if not os.path.isfile(path):
                    print("Found invalid download on,", tracks[track]["name"])
                    tracks[track].pop("download-path")
        js = json.dumps(tracks)
        df.overwrite(js)
        print("Validated", count, "entries that have download-path")

    def delete_entry(self, id):
        df = FileHelper("../data.json")
        if df.exists():
            split_id = id.split(":")
            source_playlist = split_id[0]
            source_id = split_id[1]
            data_tracks = json.loads(df.read())
            data_tracks.pop(id)
            sf = FileHelper(source_playlist+".json")
            if sf.exists():
                source_tracks = json.loads(sf.read())
                source_tracks.pop(source_id)
                js = json.dumps(source_tracks)
                sf.overwrite(js)
            js = json.dumps(data_tracks)
            df.overwrite(js)
