# -*- coding: utf-8 -*-
import mimetypes
import cStringIO as StringIO

from bottle import request, response, get, post
from bottle import static_file, redirect, HTTPResponse
#from bottle import jinja2_view as view
from bottle import mako_view as view
from PIL import Image
import pymongo
#from pymongo import ObjectId
from models import FileF7

PAGE_SIZE = 5

@get(['/', '/list', '/list/:page#\d+#'])
@view('templates/base/list.mako')
def list(page=0):
    ''' List files. '''
    page = int(page)
    prev_page = None
    next_page = None
    if page > 0:
        prev_page = page - 1
    if FileF7.objects.count() > (page + 1) * PAGE_SIZE:
        next_page = page + 1
    files = (FileF7.objects
            .order_by('-uploadDate')
            .skip(page * PAGE_SIZE)
            .limit(PAGE_SIZE))
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
    filef7.fs.files.filename = request.POST['filename']
    filef7.fs.files.text = request.POST['text']
    if 'image' in request.files:
        upload = request.files['image']
        if not upload.filename.lower().endswith(
                ('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            redirect('/')
        mime = mimetypes.guess_type(upload.filename)[0]
        filef7.fs.files.filename = upload.filename
        # Save fullsize image
        filef7.fs.files.image.put(upload.file, content_type=mime)
        # Create and save thumbnail
        image = Image.open(filef7.fs.files.image)
        image.thumbnail((80, 60), Image.ANTIALIAS)
        data = StringIO.StringIO()
        image.save(data, image.format)
        data.seek(0)
        filef7.fs.files.thumb.put(data, content_type=mime)
    filef7.fs.files.save()
    redirect('/')


@get('/:image_type#(image|thumb)#/:filename')
def get_image(image_type, filename):
    ''' Send image or thumbnail from file stored in the database. '''
    f = FileF7.objects.with_id(ObjectId(filename))[image_type]
    response.content_type = f.content_type
    return HTTPResponse(f)


@get('/static/:filename#.+#')
def get_static_file(filename):
    ''' Send static files from ./static folder. '''
    return static_file(filename, root='./static')
