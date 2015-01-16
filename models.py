# -*- coding: utf-8 -*-
import datetime
from mongoengine import Document, connect, register_connection
from mongoengine import StringField, DateTimeField, FileField

DB_NAME = 'gridfs_file7'

class FileF7(Document):
    filename = StringField(required=True)
    text = StringField(required=True)
    uploadDate = DateTimeField(required=True, default=datetime.datetime.now)
    md5 = StringField()
    image = FileField()
    thumb = FileField()



#connect(db=DB_NAME,collection='fs.files')
register_connection('default', name=DB_NAME, username='mongo', password='mongo')
print dir(register_connection)




from flask import Flask
from werkzeug.routing import BaseConverter, ValidationError
from itsdangerous import base64_encode, base64_decode
from bson.objectid import ObjectId
from bson.errors import InvalidId

class ObjectIDConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(base64_decode(value))
        except (InvalidId, ValueError, TypeError):
            raise ValidationError()
    def to_url(self, value):
        return base64_encode(value.binary)
