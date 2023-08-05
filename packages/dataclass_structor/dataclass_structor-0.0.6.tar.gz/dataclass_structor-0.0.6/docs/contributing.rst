Contributing
============

How to Contribute
-----------------

There are a lot of different ways to contribute to a project

Filing issues:
^^^^^^^^^^^^^^

If you would like to file an issue this project uses `Github issues`_ for both
feature requests and bugs.

.. _`Github Issues`: https://github.com/hockeybuggy/dataclass_structor/issues


Making code changes:
^^^^^^^^^^^^^^^^^^^^

If you want to make changes to the code start with::

    git clone dataclass_structor
    pipenv install --dev

After you make some changes create a Github pull request. After opening up the
pull request CI (continuous integration) will run some tests. In order for your
PR to be accepted it will need pass the tests, have the correct types, as well
as be formatted "correctly".

To run the tests::

    make test

To check that the types are correct::

    make typecheck  # This will run mypy

To format the code run::

    make format  # This will run black

To format the code run::

Running performance tests:
^^^^^^^^^^^^^^^^^^^^^^^^^^

This package has some performance tests that measure the performance of the
`structure` and `unstructure` functions. The intention is that these tests can
be used to see how proposed changes affect the speed execution.

To run the performance tests::
    make perf-tests

To see the results of the performance tests::
	pipenv run python -m perf show bench.json

For more perf functions see this doc:
https://perf.readthedocs.io/en/latest/cli.html


Updating documentation:
^^^^^^^^^^^^^^^^^^^^^^^

If you would like to update documentation::

    git clone dataclass_structor
    pipenv install --dev
    make build-docs


Publishing a version
^^^^^^^^^^^^^^^^^^^^

To publish a new version you need to have access to PyPi and ReadTheDocs. For
now Douglas Anderson will publish all releases for simplicity.

1. Update the `__version__` in `dataclass_structor/__init__.py`.
2. Update the `CHANGELOG.md` moving the items in the `Unreleased` section to a
   section with the version in bracets, a hyphen then the date (YYYY-MM-DD).
3. Commit these changes. Use the following template::
    Cutting version `X.Y.Z`

    User facing changes:
    https://github.com/hockeybuggy/dataclass_structor/blob/master/CHANGELOG.md#XYZ---YYYY-MM-DD
4. One this commit has landed in the master branch, create a git tag: ``git tag -s vX.Y.Z -m "Version X.Y.Z"``
5. Push the tag: ``git push --tags`
6. 


Code of Conduct
---------------

This project follows and will enforce, the Contributor Covenant:
https://github.com/hockeybuggy/dataclass_structor/CODE_OF_CONDUCT.md
