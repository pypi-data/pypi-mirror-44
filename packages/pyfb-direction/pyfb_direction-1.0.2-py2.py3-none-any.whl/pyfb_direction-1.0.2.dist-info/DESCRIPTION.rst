=============================
Pyfb-direction
=============================

.. image:: https://badge.fury.io/py/pyfb-direction.svg
    :target: https://badge.fury.io/py/pyfb-direction

.. image:: https://travis-ci.org/mwolff44/pyfb-direction.svg?branch=master
    :target: https://travis-ci.org/mwolff44/pyfb-direction

.. image:: https://codecov.io/gh/mwolff44/pyfb-direction/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mwolff44/pyfb-direction

Phonenumber's direction package

Documentation
-------------

The full documentation is at https://pyfb-direction.readthedocs.io.

Quickstart
----------

Install pyfb-direction::

    pip install pyfb-direction

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'pyfb_direction.apps.PyfbDirectionConfig',
        ...
    )

Add pyfb-direction's URL patterns:

.. code-block:: python

    from pyfb_direction import urls as pyfb_direction_urls


    urlpatterns = [
        ...
        url(r'^', include(pyfb_direction_urls)),
        ...
    ]

Features
--------

* Telephony prefix management linking prefix with destination, country, network type and Carrier
* Admin interface
* CSV import / export
* web template with Bootstrap 4
* APIs 

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




History
-------

1.0.2 (2019-03-27)
++++++++++++++++++

* Change carrier to be nullable in destination model
* Destination's screen improvements

1.0.1 (2019-01-30)
++++++++++++++++++

* SQL view for Kamailio

1.0.0 (2018-11-15)
++++++++++++++++++

* First release on PyPI.


