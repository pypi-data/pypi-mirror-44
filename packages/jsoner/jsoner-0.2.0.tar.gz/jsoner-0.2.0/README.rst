======
jsoner
======

.. image:: https://img.shields.io/travis/sschaffer92/jsoner.svg
        :target: https://travis-ci.org/sschaffer92/jsoner

.. image:: https://readthedocs.org/projects/jsoner/badge/?version=latest
        :target: https://jsoner.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/sschaffer92/jsoner/badge.svg
        :target: https://coveralls.io/github/sschaffer92/jsoner
        :alt: Coverage

* Free software: MIT license

* Documentation: https://jsoner.readthedocs.io.

*Jsoner* is a package aiming for making conversion to and from json easier.


Installation
------------


Stable release
~~~~~~~~~~~~~~

To install jsoner, run this command in your terminal:

.. code-block:: console

    $ pip install jsoner

This is the preferred method to install jsoner, as it will always install the most recent stable release.


From sources
~~~~~~~~~~~~

The sources for jsoner can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/sschaffer92/jsoner

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/sschaffer92/jsoner/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/sschaffer92/jsoner
.. _tarball: https://github.com/sschaffer92/jsoner/tarball/master


Usage
-----

*Jsoner* builds on the builtin *json* python package. Since you cannot serialize object to json by
default it can be useful to have a nice way for doing so. This package provides three different ways to
achieve this:

- provide an ``to_dict`` and ``from_dict`` method:

.. code-block:: python

    from jsoner import dumps, loads
    class A:
        def __init__(self, a):
            self.a = a

        def to_dict(self) -> dict:
            return {'a': self.a}

        @classmethod
        def from_dict(cls, data: dict) -> 'A':
            return A(**data)

    a = A(42)
    data = dumps(a)
    a = loads(data)


- or provide an ``to_str`` and ``from_str`` method:

.. code-block:: python

    from jsoner import dumps, loads
    class A:
        def __init__(self, a):
            self.a = a

        def to_str(self) -> str:
            return str(self.a)

        @classmethod
        def from_str(cls, data: str) -> 'A':
            return A(data)

    a = A('foo')
    data = dumps(a)
    a = loads(data)


- or implement a conversion function pair (This way is especially useful if
  you don't have direct access to the class definition):

.. code-block:: python

    from jsoner import dumps, loads
    from jsoner import encoders, decoders
    class A:
        def __init__(self, a):
            self.a = a

    @encoders.register(A)
    def encode_a(a: 'A') -> str:
        return a.a

    @decoders.register(A)
    def decode_a(data: str) -> str:
        return A(data)

    a = A('foo')
    data = dumps(a)
    a = loads(data)

*Jsoner* can also deal with nested objects as long they are also serializable as described above.


*Celery* and *Django*
~~~~~~~~~~~~~~~~~~~~~

One good use case for the *Jsoner* package is the *Celery* serialization of tasks and task results.

To make *Celery* use *Jsoner* you can apply the following settings:

.. code-block:: python

    from celery import app
    from kombu import serialization

    from jsoner import dumps, loads

    # register Jsoner
    serialization.register('jsoner', dumps, loads, content_type='application/json')

    app = Celery('Test')

    # tell celery to use Jsoner
    app.conf.update(
        accept_content=['jsoner'],
        task_serializer='jsoner',
        result_serializer='jsoner',
        result_backend='rpc'
    )

    # Celery can now serialize objects which can be serialized by Jsoner.
    class A:
        def __init__(self, foo):
            self.foo = foo

        @classmethod
        def from_dict(cls, data: dict) -> 'A':
            return A(**data)

        def to_dict(self):
            return {'foo': self.foo}

    a = A('bar')

    @app.task
    def task(obj: A) -> 'A':
        ...
        return obj

    a = task.delay(a).get()


This way you can easily serialize django model instances and pass them to the
*Celery* task.

.. code-block:: python
   :name: models.py

    from django.db import models

    class Person(models.Model):
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)


Then you can just pass the model to the celery task directly:

.. code-block:: python

    from django.db.models import Model
    from jsoner import encoders, decoders

    from .models import Person

    # Create a conversion function pair which just saved the primary key.
    @encoders.register(Model)
    def to_primary_key(model: Model) -> int:
        return model.pk

    # Load object from the primary key.
    @decoders.register(Model)
    def from_primary_key(pk: int, model_cls: Model) -> Model:
        return model_cls.objects.get(pk=pk)

    p = Person(first_name="Foo", last_name="Bar")
    p = task.delay(p).get()


Similar you could create a conversion function pair for querysets.
