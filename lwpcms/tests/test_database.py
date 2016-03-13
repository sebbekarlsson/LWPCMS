import unittest
from lwpcms.tests.mock.mongo import db


def test_connection():
    db.collections.insert_one({'name': 'test'})

    test = db.collections.find_one({'name': 'test'})

    assert test != None

    db.collections.delete_many({'name': 'test'})
    test = db.collections.find_one({'name': 'test'})

    assert test == None
