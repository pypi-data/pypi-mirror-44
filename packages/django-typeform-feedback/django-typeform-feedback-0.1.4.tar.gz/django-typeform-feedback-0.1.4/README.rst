=============================
django-typeform-feedback
=============================

.. image:: https://badge.fury.io/py/django-typeform-feedback.svg
    :target: https://badge.fury.io/py/django-typeform-feedback

.. image:: https://requires.io/github/exolever/django-typeform-feedback/requirements.svg?branch=master
     :target: https://requires.io/github/exolever/django-typeform-feedback/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://travis-ci.org/exolever/django-typeform-feedback.svg?branch=master
    :target: https://travis-ci.org/exolever/django-typeform-feedback

.. image:: https://codecov.io/gh/exolever/django-typeform-feedback/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/exolever/django-typeform-feedback

.. image:: https://sonarcloud.io/api/project_badges/measure?project=exolever_django-typeform-feedback&metric=alert_status
   :target: https://sonarcloud.io/dashboard?id=exolever_django-typeform-feedback
  
.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
   :target: https://github.com/exolever/django-typeform-feedback/issues
    
.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://opensource.org/licenses/MIT

Use typeform as feedback with Django

Quickstart
----------

Install django-typeform-feedback::

    pip install django-typeform-feedback

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'typeform_feedback',
        ...
    )

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
