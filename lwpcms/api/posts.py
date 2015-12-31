from lwpcms.models import sess, Post, User
from lwpcms.api.modules import call_module_event
from lwpcms.api.constants import hooks


def publish_post(title, content, id=None):
    if id is not None:
        post = sess.query(Post).filter(Post.id==id).first()
        post.title=title
        post.content=content
    else:
        post = Post(
                title=title,
                content=content,
                type='post',
                author_id=0
                )

    call_module_event(hooks['post_publish'], {'post': post})
    sess.add(post)
    sess.commit()

    return post
