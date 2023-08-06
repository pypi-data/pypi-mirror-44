
restible-sqlalchemy
###################

.. readme_inclusion_marker


**restible-sqlalchemy** is a library that provides **django** integration with
`restible <https://github.com/novopl/restible>`_. It includes the base resource
class ``SqlAlchemyResource`` that can be used to define REST resources based on
SQLAlchemy model definitions.


.. note::
    The CircleCI builds can be found
    `here <https://circleci.com/gh/novopl/restible-sqlalchemy>`_

Installation
============

.. code-block:: shell

    $ pip install restible-sqlalchemy


Contributing
============

Setting up development repo
---------------------------

.. code-block:: shell

    $ git clone git@github.com:novopl/restible-sqlalchemy.git
    $ cd restible-sqlalchemy
    $ virtualenv env
    $ source ./env/bin/activate
    $ pip install -r requirements.txt -r ops/devrequirements.txt
    $ peltak git add-hooks


Running tests
.............

**Config**: The types of tests are defined in ``pelconf.py`` and the
pytest configuration is defined in ``ops/tools/pytest.ini``.

.. code-block:: shell

    $ peltak test

Linting
.......

**Config**: The list of locations to lint is defined in ``pelconf.py`` and the
linters configuration is defined in ``ops/tools/{pylint,pep8}.ini``.

.. code-block:: shell

    $ peltak lint

Generating docs
...............

**Config**: The list of documented files and general configuration is in
``pelconf.py`` and the Sphinx configuration is defined in ``docs/conf.py``.

.. code-block:: shell

    $ peltak docs
