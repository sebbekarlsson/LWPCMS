from lwpcms.models import sess, Post, User


def publish_post(title, content):
    post = Post(
            title=title,
            content=content,
            type='post',
            author_id=0
            )
    sess.add(post)
    sess.commit()

    return post
