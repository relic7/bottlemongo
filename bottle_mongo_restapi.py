#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import bottle
from bottle import route, run, request, abort
import pymongo

def connect_gridfs_mongodb(hostname=None,db_name=None):
    import pymongo, gridfs, __builtin__
    if not hostname:
        hostname = '127.0.0.1'
    if not db_name:
        db_name = 'gridfs_file7'
    mongo = pymongo.MongoClient(hostname, max_pool_size=50, waitQueueMultiple=10)
    mongo_db = mongo[db_name]
    #mongo_db = mongo[db_name]
    mongo_db.authenticate('mongo', 'mongo')
    fs = ''
    fs = gridfs.GridFS(mongo_db)
    return mongo_db, fs

db,fs = connect_gridfs_mongodb(hostname=None,db_name=None)


@route('/list', method='GET')
def list(page=0):
    ''' List files. '''
    page = int(page)
    prev_page = None
    next_page = None
    if page > 0:
        prev_page = page - 1
    if len(fs.list) > (page + 1) * PAGE_SIZE:
        next_page = page + 1
    files = (db['fs.files'].objects
            .order_by('-uploadDate')
            .skip(page * PAGE_SIZE)
            .limit(PAGE_SIZE))
    return {'files': files,
            'prev_page': prev_page,
            'next_page': next_page,
            }


@route('/filesf7', method='PUT')
def put_document():
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    if not entity.has_key('_id'):
        abort(400, 'No _id specified')
    try:
        db['fs.files'].save(entity)
    except pymongo.ValidationError as ve:
        abort(400, str(ve))

@route('/filesf7/:id', method='GET')
def get_document(id):
    entity = db['fs.files'].find_one({'_id':id})
    if not entity:
        abort(404, 'No document with id %s' % id)
    return entity

run(host='localhost', port=8080)
