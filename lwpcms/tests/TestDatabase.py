import unittest
from lwpcms.tests.mock.mongo import db

class TestDatabase(unittest.TestCase):


  def test_connection(self):
      db.collections.insert_one({'name': 'test'})

      test = db.collections.find_one({'name': 'test'})

      self.assertNotEqual(test, None)

      db.collections.delete_many({'name': 'test'})
      test = db.collections.find_one({'name': 'test'})

      self.assertEqual(test, None)
