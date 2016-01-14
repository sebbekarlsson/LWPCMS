from lwpcms.api.modules import call_module_event
from lwpcms.api.constants import hooks
from lwpcms.mongo import db
from bson.objectid import ObjectId


def publish_post(title, content, attachments, id=None):
    if id is not None:
        post = db.collections.update_one(
                {
                    "_id": ObjectId(id)    
                },
                {
                    "$set": {
                        "title": title,
                        "content": content
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
        post = {
                "classes": ["post"],
                "title": title,
                "content": content,
                "attachments": attachments,
                "author": {}
            }

        call_module_event(hooks['post_publish'], {'post': post})
        db.collections.insert_one(post)

    return post
