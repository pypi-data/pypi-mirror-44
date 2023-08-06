=============================
django-inclusion-block-tag
=============================

.. image:: https://badge.fury.io/py/django-inclusion-block-tag.svg
    :target: https://badge.fury.io/py/django-inclusion-block-tag

.. image:: https://travis-ci.org/bmihelac/django-inclusion-block-tag.svg?branch=master
    :target: https://travis-ci.org/bmihelac/django-inclusion-block-tag

.. image:: https://codecov.io/gh/bmihelac/django-inclusion-block-tag/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/bmihelac/django-inclusion-block-tag

Your project description goes here

Documentation
-------------

...

   The full documentation is at https://django-inclusion-block-tag.readthedocs.io.

Quickstart
----------

Install django-inclusion-block-tag::

    pip install django-inclusion-block-tag

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'inclusion_block_tag.apps.InclusionBlockTagConfig',
        ...
    )


See test_tags.py.

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
