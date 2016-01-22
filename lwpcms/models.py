import time
import json


class DBObject(object):
    def __init__(self, classes, type):
        self.created = time.strftime("%Y:%m:%d:%H:%M:%S")
        self.updated = ''
        self.classes = classes
        self.type = type
    

    def export(self):
        return self.__dict__


class Post(DBObject):
    def __init__(self, title, content, attachments, author, type, classes):
        DBObject.__init__(self, classes, type)
        self.title = title
        self.content = content
        self.attachments = attachments
        self.author = author
