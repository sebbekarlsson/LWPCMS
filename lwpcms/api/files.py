from lwpcms.models import sess, Post, User
from werkzeug import secure_filename

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

        file_post = Post(
            title = title,
            content = filename,
            type = 'file',
            author_id = 0
        )

        sess.add(file_post)
        sess.commit()

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
