import pytest
from lwpcms.api.user import register_user
from lwpcms.mongo import db


def test_registration():
    nick = 'JohnDoe'
    user = register_user(name=nick, password='dot')

    assert user != None

    db_user = db.collections.find(
          {'structure': '#User', 'nick_name': nick}
          )

    assert db_user != None

    db.collections.delete_many(
          {'structure': '#User', 'nick_name': nick}
          )
