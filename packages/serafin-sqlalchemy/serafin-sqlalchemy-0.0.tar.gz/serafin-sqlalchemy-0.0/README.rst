
##################
serafin-sqlalchemy
##################

**serafin-appengine** is a small python library that provides SQLAlchemy
models integration for `serafin <https://github.com/novopl/serafin>`_.

.. note::
    The CircleCI builds can be found
    `here <https://circleci.com/gh/novopl/serafin-sqlalchemy>`_

.. readme_inclusion_marker

Installation
============

.. code-block:: shell

    $ pip install serafin-sqlalchemy


Contributing
============

Setting up development repo
---------------------------

.. code-block:: shell

    $ git clone git@github.com:novopl/serafin-sqlalchemy.git
    $ cd serafin-sqlalchemy
    $ virtualenv env
    $ source ./env/bin/activate
    $ pip install -r ops/devrequirements.txt
    $ peltak git add-hoooks


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
