from lwpcms.api.modules import call_module_event
from lwpcms.api.constants import hooks
from lwpcms.mongo import db
from lwpcms.models import Post, Option
from bson.objectid import ObjectId
import re


""" Return Object
This function is used to publish a post.
"""
def publish_post(title, content, attachments, published=True, tags=[], id=None):
    if id is not None:
        post = db.collections.update_one(
                {
                    "_id": ObjectId(id)    
                },
                {
                    "$set": {
                        "title": title,
                        "content": content,
                        "published": published,
                        "tags": tags
                    }
                }
            )
        for attachment in attachments:
            post = db.collections.update_one(
                {
                    "_id": ObjectId(id)    
                },
                {
                    "$addToSet": {
                        "attachments": attachment
                    }
                }
            )
        return {"_id": ObjectId(id) }
    else:
        post = Post(
                classes=["post"],
                type='post',
                title=title,
                content=content,
                attachments=attachments,
                tags=tags,
                author={},
                published=published
                ).export()

        call_module_event(hooks['post_publish'], {'post': post})
        db.collections.insert_one(post)

    return post


def get_posts(obj, sort=None):
    """ Return list
    This function is used to query for posts.
    """
    if sort is not None:
        return list(db.collections.find(obj).sort(*sort))
    else:
        return list(db.collections.find(obj))


def get_option(name):
    """ Return dict
    This function is used to fetch an option.
    """
    option = list(
            db.collections.find(
                    {
                        'key': name,
                        'structure': '#Option'
                    }
                )
            )

    if len(option) > 0:
        return option[0]
    else:
        return None


def set_option(name, value, type='text', editable=True):
    """ Return void
    This function is used to set/create an option.
    """
    old = db.collections.find_one({
            'key': name,
            'structure': '#Option'
        })

    if old is not None:
        type = old['type']

    return db.collections.update_one(
            {
                'key': name,
                'structure': '#Option'
            },
            {
                '$set': {'value': value, 'type': type, 'editable': editable}
            },
            True
        )


def shorten_text(text, max=16):
    """ Return String
    This function is used to shorten a text, creating a teaser.
    """
    return (text[:max] + '..') if len(text) > max else text


def render_content(content):
    """ Return String
    This function is used to render content, from a post or just anything.
    """
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            content)

    for url in urls:
        if  any(x in url for x in ['youtube', 'watch']):
            embed = url.replace('watch?v=', 'embed/')
            content = content.replace(
            url,
            '''
            <iframe width="420" height="315" src="{url}">
            </iframe><br>
            '''.format(url=embed))

    content = content.replace('\n', '<br>')

    return content
