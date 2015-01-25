# -*- coding: utf-8 -*-
import mimetypes
import cStringIO as StringIO

from bottle import request, response, get, post
from bottle import static_file, redirect, HTTPResponse
#from bottle import jinja2_view as view
from bottle import mako_view as view
from PIL import Image
import pymongo
<<<<<<< HEAD
from pymongo import ObjectId
=======
from bson.objectid import ObjectId
#from pymongo import ObjectId
>>>>>>> e0215f6df321826cc6f8f0076a3a21b49bbfda90
from models import FileF7

### Basic Authd Connect to Mongo, return db and/or fs.files etc
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


PAGE_SIZE = 5

@get(['/', '/list', '/list/:page#\d+#'])
@view('templates/base/results.html')
def list(page=0):
    ''' List files. '''
    coll = db['fs.files']
    page = int(page)
    prev_page = None
    next_page = None
    if page > 0:
        prev_page = page - 1
    if coll.count() > (page + 1) * PAGE_SIZE:
        next_page = page + 1
    i = iter(coll.find())
    files = i.sort('-uploadDate').skip(page * PAGE_SIZE).limit(PAGE_SIZE)
    return {'files': files,
            'prev_page': prev_page,
            'next_page': next_page,
            }




@post('/create')
def create():
    ''' Save new Image. '''
    if not (request.POST.get('filename') and request.POST.get('text')):
        redirect('/')
    filef7 = FileF7()
    print dir(filef7)
    db['fs.files'].filename = request.POST['filename']
    db['fs.files'].text = request.POST['text']
    if 'image' in request.files:
        upload = request.files['image']
        if not upload.filename.lower().endswith(
                ('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            redirect('/')
        mime = mimetypes.guess_type(upload.filename)[0]
        db['fs.files'].filename = upload.filename
        # Save fullsize image
        db['fs.files'].image.put(upload.file, content_type=mime)
        # Create and save thumbnail
        image = Image.open(db['fs.files'].image)
        image.thumbnail((80, 60), Image.ANTIALIAS)
        data = StringIO.StringIO()
        image.save(data, image.format)
        data.seek(0)
        db['fs.files'].thumb.put(data, content_type=mime)
    db['fs.files'].save()
    redirect('/')


@get('/:image_type#(image|thumb)#/:filename')
def get_image(image_type, filename):
    ''' Send image or thumbnail from file stored in the database. '''
    f = db['fs.files'].objects.with_id(ObjectId(filename))[image_type]
    response.content_type = f.content_type
    return HTTPResponse(f)


@get('/static/:filename#.+#')
def get_static_file(filename):
    ''' Send static files from ./static folder. '''
    return static_file(filename, root='./static')
