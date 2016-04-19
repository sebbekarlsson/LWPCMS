from werkzeug import secure_filename

from lwpcms.mongo import db
from lwpcms.models import Post, File
from bson.objectid import ObjectId

import time
import os

import tarfile

from PIL import Image


def file_thumbnail(file, size):
    """ Return String
    This function is used to get a thumbnailname for an image.
    """
    fname = file.split('.')[0]
    ext = file.split('.')[1]

    thumb_name = '{}_{}{}'.format(fname, '{}x{}'.format(size, size), '.' + ext)

    return thumb_name


def is_image(filename):
    """ Return Boolean
    This function is used to check if an image is an image.
    """
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
    """ Return void
    This function is used to generate thumbnails for a specific imagefile.
    """
    sizes = [(128,128), (64,64), (32,32)]

    for size in sizes:
      img = Image.open(file)
      img.thumbnail(size)
      fname = file.split('.')[0]
      ext = file.split('.')[1]
      img.save("{}_{}{}".format(fname, '{}x{}'.format(*size), '.' + ext))


def upload_file(file):
    """ Return Boolean
    This function is used to upload and save a file.
    """
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

        db_file = File(filename=filename).export()
        
        db.collections.insert_one(db_file)

        return True
    else:
        return False


def make_tarfile(output_filename, source_dir):
    """ Return void
    This function is used to create a tar file from a directory.
    """
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
