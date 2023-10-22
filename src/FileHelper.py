import os


class FileHelper:
    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, content):
        f = open(self.file_name, 'a')
        f.write(content + '\n')
        f.close()

    def overwrite(self, content):
        f = open(self.file_name, 'w')
        f.write(content + '\n')
        f.close()

    def read(self):
        f = open(self.file_name, 'r')
        return f.read()

    def exists(self):
        return os.path.isfile(self.file_name)
