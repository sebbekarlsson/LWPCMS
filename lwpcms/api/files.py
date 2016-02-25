from werkzeug import secure_filename

from lwpcms.mongo import db
from lwpcms.models import Post
from bson.objectid import ObjectId

import time
import os

from PIL import Image


def file_thumbnail(file, size):
    fname = file.split('.')[0]
    ext = file.split('.')[1]

    thumb_name = '{}_{}{}'.format(fname, '{}x{}'.format(size, size), '.' + ext)

    return thumb_name


def is_image(filename):
    image_extensions = [
                '.jpg',
                '.jpeg',
                '.png',
                '.gif',
                '.bmp',
                '.svg',
                '.ico'
            ]
    filename, file_extension = os.path.splitext(filename)
    
    if file_extension in image_extensions or file_extension in\
            [extension.upper() for extension in image_extensions]:
                return True

    return False


def generate_thumnails(file):
    sizes = [(128,128), (64,64), (32,32)]

    for size in sizes:
      img = Image.open(file)
      img.thumbnail(size)
      fname = file.split('.')[0]
      ext = file.split('.')[1]
      img.save("{}_{}{}".format(fname, '{}x{}'.format(*size), '.' + ext))


def upload_file(file, title):
    if file:        
        filename = secure_filename(
            time.strftime("%H:%M:%S")\
            + '_' +
            file.filename
        )

        saved_file = os.path.join('lwpcms/static/upload', filename)
        file.save(saved_file)

        if is_image(saved_file):
            generate_thumnails(saved_file)

        post = Post(
                    classes=["post", "file"],
                    type='file',
                    title=title,
                    content=filename,
                    attachments={},
                    author={},
                    meta={'original_filename': file.filename}
                ).export()
        
        db.collections.insert_one(post)

        return True
    else:
        return False
