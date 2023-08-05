============
@environment
============


.. image:: https://img.shields.io/pypi/v/atenvironment.svg
        :target: https://pypi.python.org/pypi/atenvironment

.. image:: https://img.shields.io/travis/eghuro/atenvironment.svg
        :target: https://travis-ci.org/eghuro/atenvironment

.. image:: https://readthedocs.org/projects/atenvironment/badge/?version=latest
        :target: https://atenvironment.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/eghuro/atenvironment/shield.svg
     :target: https://pyup.io/repos/github/eghuro/atenvironment/
     :alt: Updates


.. image:: https://codecov.io/gh/eghuro/atenvironment/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/eghuro/atenvironment



Decorator for convenient loading of environment variables.
@environment allows you to declare dependencies on environment variables so that it's clear what needs to be set. Also, any error handling is moved away making the code clearer.


* Free software: MIT license
* Documentation: https://atenvironment.readthedocs.io.


Getting started
---------------
Install @environment from pip:

   pip install atenvironment


Using @environment is as simple as::

  from atenvironment import environment

  @environment('API_KEY', 'TOKEN')
  def check(a, b, c, key, token):
      # API_KEY is in key
      # TOKEN is in token

Then call the function as::

   check(a, b, c)

Environment variables are checked and provided to the function as trailing parameters in order of declaration. In case the token is not in environment an ``atenvironment.EnvironMiss`` exception is raised.
You can also provide your own error handling function. In addition, some environment variables can be loaded directly into object variable in case instance property is to be initialized.


See the docummentation for more details.
