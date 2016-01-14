import os
from setuptools import setup


setup(
    name='LWPCMS',
    version='1.0',
    description='Lightweight Python Content Management System',
    author='Sebastian Robert Karlsson',
    author_email='sebbekarlsson97@gmail.com',
    url='http://www.ianertson.com/',
    install_requires=[
        'flask',
        'flask-wtf',
        'wtforms',
        'PyMySQL',
        'sqlalchemy',
        'pyyaml',
        'loremipsum',
        'pymongo'
    ]
)
