# SQLtills

## Simple CRUD utilities for sqlalchemy

Finding myself having to duplicate code for my projects for CRUD even when using SQLAlchemy was very annoying. Thus I created some utilities which I then found annoying to have to copy paste and maintain between different projects. So in all my selfish glory I present to you SQLtills, a simple CRUD tool for sqlalchemy. Why is it called SQLtills because I am extremly horrible at naming things.

SQLtills is available on PyPi so to install simply:

```sh
pip install -U SQLtills
```

## How to use sqltills

For this tutorial we will be using an in-memory sqlite database as is typical for an sqlalchemy tutorial however, and this probably doesn't need to be said, we're good with whatever sqlalchemy is good with.

Imagine you have a database with two tables: authors and blogs

your sqlalchemy models would then be

```python

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key = True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    title = Column(String)
    blog_text = Column(String)

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    blogs = relationship(Blog, backref = backref("author", uselist = False))

engine = create_engine('sqlite:///:memory:', echo=True)

Base.metadata.bind = engine

Base.metadata.create_all()

```

Awesome we now have the two tables in the database and the models defined. In the same script lets write some basic CRUD  you would do in an app using sqltills utilities

```python
from sqltills import create_rows

session_maker = sessionmaker(bind = engine)
session = sessionmaker()

new_author = Author()
new_author.name = "Omar"

new_blog = Blog()
new_blog.title = "How SQLAlchemy is Totally Awesome"
new_blog.blog_text = "too much stuff to put into one blog so the short answer is because"

new_author.blogs.append(new_blog)

create_rows(sesion, new_author, new_blog)

```

Easy right ! Okay imagine my application explodes and becomes medium.com now I have thousands of blogs and thousands of authors. I want to get all blogs which have the author being either Omar or Nancy

```python

from sqltills import read_rows

results = read_rows(session, Author, filters = [
    {
        'name': {
            'comparitor': '==',
            'data': 'Omar'
        },
    'join': 'or'
    },
    {
        'name': {
            'comparitor':'==',
            'data': 'Nancy'
        }
    }
])

results = results.all()

for author in results:
    for blog in author.blogs:
        print(blog.title)
```

The filters argument is optional, if excluded the whole table will be included in the SQLAlchemy Query object. A parse-(like)-tree is used to build the filter expressions used in the session.query().filter() method

This filter parser can be used as well.

```python

from sqltills import ParseTree
filters = [
    {
        'name': {
            'comparitor': '==',
            'data': 'Omar'
        },
    'join': 'or'
    },
    {
        'name': {
            'comparitor':'==',
            'data': 'Nancy'
        }
    }
]
parser = ParseTree(Author, filters)
results = parser.query(session)

```

This is a really simple and almost useless package but it allows me to have a centralized set of tools to do all my CRUD and makes my code clean(er) and easier to maintain.
