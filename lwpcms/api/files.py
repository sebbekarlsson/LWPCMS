from werkzeug import secure_filename

from lwpcms.mongo import db
from lwpcms.models import Post
from bson.objectid import ObjectId

import time
import os


def upload_file(file, title):
    if file:        
        filename = secure_filename(
            time.strftime("%H:%M:%S")\
            + '_' +
            file.filename
        )

        file.save(os.path.join('lwpcms/static/upload', filename))

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
