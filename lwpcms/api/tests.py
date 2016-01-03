from loremipsum import get_sentence
import glob
import os
import shutil
from lwpcms.models import sess, Post


def generate_files():
    for filename in glob.iglob('lwpcms/tests/shards/image/*'):
        filename = os.path.basename(filename)
        shutil.copy2('lwpcms/tests/shards/image/{}'.format(filename),
                'lwpcms/static/upload/{}'.format(filename))

        file_post = Post(
            title = get_sentence(),
            content = filename,
            type = 'file',
            author_id = 0
        )

        sess.add(file_post)
        sess.commit()
