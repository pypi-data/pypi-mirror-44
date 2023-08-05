=========
 hatcher
=========

Surprisingly, a client to talk to the brood server.

Setup
-----

Create the development environment with the desired python version::

  edm env create hatcher-dev --version=2 --force
  edm run -e hatcher-dev -- pip install -e .
  edm run -e hatcher-dev -- python -m hatcher --help

.. note::

   - A recent EDM is recommended, but a normal python or
     virtualenv environment can be also used.

Test
----

Run the tests in the development environment::

  edm run -e hatcher-dev -- pip install -r test_requirements.txt
  edm run -e hatcher-dev -- haas -v hatcher

Documentation
-------------

To build the documentation we need sphinx > 1.6.6 to be installed::

  edm run -e hatcher-dev -- pip install -r doc_requirements.txt
  edm run -e hatcher-dev -- python setup.py build_sphinx --fresh-env


Basic Usage
-----------

When used in production, the latest **release** tag must be used. For
example, a tag such as ``v0.3.0`` must be used, rather than
``v0.4.0.dev419``.  In all of the following examples, the
``https://brood-dev`` URL must be substituted with a valid server URL.

To get a basic idea of usage::

    hatcher --help

To list the repositories to which the authenticated user has access::

    hatcher --url https://brood-dev user repositories

To upload an egg::

    # Upload a free rh5-x86 egg
    hatcher --url https://brood-dev eggs upload enthought dev rh5-x86 dummy-1.0.1-1.egg

To list existing eggs in a repository::

    # List eggs in the enthought/dev repository for rh5-x86_64 platform (CPython 2.7).
    hatcher --url https://brood-dev eggs list enthought dev rh5-x86_64 cp27

To create a new repository and upload eggs to it::

    # List the repositories (requires administrative permissions on the organization)
    hatcher --url https://brood-dev repositories list enthought
    # Create a new repository (requires administrative permissions on the organization)
    hatcher --url https://brood-dev repositories create enthought \
        geocanopy_dev "the official geocanopy_dev repository"
    # Push some new eggs (requires upload permissions on the repository)
    hatcher --url https://brood-dev eggs batch-upload enthought \
        geocanopy_dev win-x86 egg1-1.0.1-1.egg [egg2 ...]
