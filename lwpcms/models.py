import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()
engine = sa.create_engine('sqlite:///{}.sqlite'.format('lwpcms'),
        connect_args={'check_same_thread': False})


def initialize_database():
    Base.metadata.create_all(engine)


def new_session():
    
    Session = sessionmaker()
    Session.configure(bind=engine)

    return Session()


class Data():
    created = sa.Column(sa.TIMESTAMP, server_default=sa.func.now(),
            onupdate=sa.func.current_timestamp())


class User(Base, Data):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(128))
    last_name = sa.Column(sa.String(128))
    password = sa.Column(sa.String(256))


class Post(Base, Data):
    __tablename__ = 'posts'
    id = sa.Column(sa.Integer, primary_key=True)
    parent_id = sa.Column(sa.Integer, sa.ForeignKey('posts.id'))
    title = sa.Column(sa.String(256))
    content = sa.Column(sa.String(1024))
    type = sa.Column(sa.String(256))
    author_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    attachments = relationship('Post')


sess = new_session()
