import unittest
from lwpcms.api.user import register_user
from lwpcms.mongo import db

class TestUser(unittest.TestCase):


  def test_registration(self):
      nick = 'JohnDoe'

      user = register_user(name=nick, password='dot')
      
      self.assertNotEqual(user, None)

      db_user = db.collections.find(
              {'structure': '#User', 'nick_name': nick}
              )
      
      self.assertNotEqual(db_user, None)

      db.collections.delete_many(
              {'structure': '#User', 'nick_name': nick}
              )
