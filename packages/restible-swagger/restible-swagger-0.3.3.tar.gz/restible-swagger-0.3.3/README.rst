
restible-swagger
################

.. readme_inclusion_marker

This is simple tool that makes it easy to generate OpenAPI (previously Swagger)
specification from the `restible <https://github.com/novopl/restible>`_ powered
backend code.

.. note::

    The CircleCI builds can be found
    `here <https://circleci.com/gh/novopl/restible-swagger>`_

Installation
============

.. code-block:: shell

    $ pip install restible-appengine


Contributing
============

Cloning and setting up the development repo
-------------------------------------------

.. code-block:: shell

    $ git clone git@github.com:novopl/restible-swagger.git
    $ cd restible-swagger
    $ virtualenv env
    $ source ./env/bin/activate
    $ pip install .
    $ pip install -r ops/devrequirements.txt
    $ peltak git add-hooks

.. note::
    God knows why, installing the current package with
    ``python setup.py develop`` or ``python setup.py install`` will cause pylint
    to think **six** is a local project package and it will throw errors about
    the wrong import order.


Running tests
.............

.. code-block:: shell

    $ peltak test

Linting
.......

.. code-block:: shell

    $ peltak lint

Generating docs
...............

.. code-block:: shell

    $ peltak docs
