import time
import json


class DBObject(object):
    """This class defines how objects in the mongoDB should be represented."""

    def __init__(
            self,
            classes=[],
            type='',
            meta={}
            ):
        self.created = time.strftime("%Y/%B/%d")
        self.updated = time.strftime("%Y/%B/%d")
        self.classes = classes
        self.type = type
        self.meta = meta
        self.structure = self.__class__.__name__


    def export(self):
        """This function exports the object as a dict. This is used when
        putting an object in the database."""

        return self.__dict__


class Post(DBObject):

    def __init__(
            self,
            title='',
            content='',
            attachments=[],
            author={},
            tags=[],
            published='',
            classes=[],
            type='',
            meta={}
            ):
        DBObject.__init__(self, classes, type, meta)
        self.title = title
        self.content = content
        self.attachments = attachments
        self.author = author
        self.tags = tags
        self.published = published


class User(DBObject):

    def __init__(
            self,
            nick_name='',
            first_name='',
            last_name='',
            password='',
            classes=[],
            type='',
            meta={}
            ):
        DBObject.__init__(self, classes, type, meta)
        self.nick_name = nick_name
        self.first_name = first_name
        self.last_name = last_name
        self.password = password


class Option(DBObject):

    def __init__(
            self,
            key='',
            value='',
            classes=[],
            type='',
            meta={}
            ):
        DBObject.__init__(self, classes, type, meta)
        self.key = key
        self.value = value
