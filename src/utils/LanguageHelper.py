import json
from src.utils.FileHelper import *


class LanguageHelper:
    def __init__(self, lang_code):
        lang_file = FileHelper("language_"+lang_code+".json")
        if not lang_file.exists():
            lang_file = FileHelper("../resources/language_en_us.json")
        self.lang_obj = json.loads(lang_file.read())

    def get(self, text):
        print(text)
        try:
            print(self.lang_obj[text])
            return self.lang_obj[text]
        except:
            return text

