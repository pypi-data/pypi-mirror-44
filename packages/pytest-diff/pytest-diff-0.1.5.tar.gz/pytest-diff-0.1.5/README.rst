===========
pytest-diff
===========

.. image:: https://img.shields.io/pypi/v/pytest-diff.svg
    :target: https://pypi.org/project/pytest-diff
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-diff.svg
    :target: https://pypi.org/project/pytest-diff
    :alt: Python versions

.. image:: https://travis-ci.org/username/pytest-diff.svg?branch=master
    :target: https://travis-ci.org/username/pytest-diff
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/username/pytest-diff?branch=master
    :target: https://ci.appveyor.com/project/username/pytest-diff/branch/master
    :alt: See Build Status on AppVeyor

A simple plugin to use with pytest

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* Readable diffs for failed tests
* Customizable diffs for your classes


Requirements
------------

* `pytest`
* `deepdiff`
* `pprintpp`

Installation
------------

You can install "pytest-diff" via `pip`_ from `PyPI`_::

    $ pip install pytest-diff


Usage
-----


.. code-block:: python
    class Person:
        def __init__(self, name, age, favorites):
            self.name = name
            self.age = age
            self.favorites = favorites


    def test_person():
        a = Person("Alice", age=21, favorites={"food": "spam", "movie": "Life of Brian"})
        b = Person("Alice", age=21, favorites={"food": "eggs", "movie": "Life of Brian"})
        assert a == b


Running `pytest` gives:


.. code-block:: python
    ______________________________ test_person ______________________________

        def test_person():
            a = Person("Alice", age=21, favorites={'food': 'spam', 'movie': 'Life of Brian'})
            b = Person("Alice", age=21, favorites={'food': 'eggs', 'movie': 'Life of Brian'})
    >       assert a == b
    E       assert
    E         <test_person.Person object at 0x7fa326d769e8>
    E         ==
    E         <test_person.Person object at 0x7fa326d76be0>
    E         {'values_changed': {"root.favorites['food']": {'new_value': 'spam', 'old_value': 'eggs'}}}

    examples/test_person.py:11: AssertionError





Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-diff" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/username/pytest-diff/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
