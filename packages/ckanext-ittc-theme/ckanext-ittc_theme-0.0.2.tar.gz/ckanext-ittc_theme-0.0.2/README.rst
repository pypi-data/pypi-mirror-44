.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://pypip.in/download/ckanext-ittc_theme/badge.svg
    :target: https://pypi.python.org/pypi//ckanext-ittc_theme/
    :alt: Downloads

.. image:: https://pypip.in/version/ckanext-ittc_theme/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-ittc_theme/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/ckanext-ittc_theme/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-ittc_theme/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/ckanext-ittc_theme/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-ittc_theme/
    :alt: Development Status

.. image:: https://pypip.in/license/ckanext-ittc_theme/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-ittc_theme/
    :alt: License

=============
ckanext-ittc_theme
=============

.. The theme and dataset schemas for the ITTC CKAN instance


------------
Requirements
------------

Built for CKAN version 2.8.2


------------
Installation
------------

To install ckanext-ittc_theme:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-ittc_theme Python package into your virtual environment::

     pip install ckanext-ittc_theme

3. Add ``ittc_theme`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload

If you wish to use the Schemas you will need to install https://github.com/ckan/ckanext-scheming


---------------
Config Settings
---------------

Currently no custom config


------------------------
Development Installation
------------------------

To install ckanext-ittc_theme for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/SamuelBradley/ckanext-ittc_theme.git
    cd ckanext-ittc_theme
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.ittc_theme --cover-inclusive --cover-erase --cover-tests


----------------------------------------
Releasing a New Version of ckanext-ittc_theme
----------------------------------------

ckanext-ittc_theme is availabe on PyPI as https://pypi.python.org/pypi/ckanext-ittc_theme.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
