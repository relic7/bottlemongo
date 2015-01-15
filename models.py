# -*- coding: utf-8 -*-
import datetime
from mongoengine import Document, connect
from mongoengine import StringField, DateTimeField, FileField

DB_NAME = 'gridfs_file7'

class FileF7(Document):
    filename = StringField(required=True)
    text = StringField(required=True)
    uploadDate = DateTimeField(required=True, default=datetime.datetime.now)
    md5 = StringField()
    image = FileField()
    thumb = FileField()

connect(DB_NAME)
