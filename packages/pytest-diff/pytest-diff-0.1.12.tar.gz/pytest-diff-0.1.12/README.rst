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


Running :code:`pytest` gives:


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


To customize diffs for a specific type, register it with the registry:

.. code-block:: python

    import pytest_diff


    class Car:
        def __init__(self, make, model, year):
            self.make = make
            self.model = model
            self.year = year


    @pytest_diff.registry.register(Car)
    def diff(x, y):
        lines = []

        return [f"{x.make} vs {y.make}", f"{x.model} vs {y.model}", f"{x.year} vs {y.year}"]


    def test_car():
        c1 = Car("Toyota", "Prius", 2010)
        c2 = Car("Honda", "Accord", 2009)
        assert c1 == c2





Then running :code:`pytest` shows your custom diff:

.. code-block:: python

        def test_car():
            c1 = Car("Toyota", "Prius", 2010)
            c2 = Car("Honda", "Accord", 2009)
    >       assert c1 == c2
    E       assert
    E         <test_custom.Car object at 0x7f0e9b0ccd68>
    E         ==
    E         <test_custom.Car object at 0x7f0e9b0cceb8>
    E         Toyota vs Honda
    E         Prius vs Accord
    E         2010 vs 2009

    examples/test_custom.py:21: AssertionError


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
