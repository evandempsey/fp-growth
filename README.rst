===============================
FP-Growth
===============================

.. image:: https://img.shields.io/pypi/v/pyfpgrowth.svg
        :target: https://pypi.python.org/pypi/pyfpgrowth

.. image:: https://img.shields.io/travis/evandempsey/fp-growth.svg
        :target: https://travis-ci.org/evandempsey/fp-growth

.. image:: https://readthedocs.org/projects/fp-growth/badge/?version=latest
        :target: https://readthedocs.org/projects/fp-growth/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/evandempsey/fp-growth/badge.svg
        :target: https://coveralls.io/github/evandempsey/fp-growth

A Python implementation of the Frequent Pattern Growth algorithm.

* Free software: ISC license
* Documentation: https://fp-growth.readthedocs.org.

Getting Started
---------------

You can install the package with pip::

    pip install pyfpgrowth

Then, to use it in a project, inport it and use the find_frequent_patterns and generate_association_rules functions::

    import pyfpgrowth

It is assumed that your transactions are a sequence of sequences representing items in baskets. The item IDs are integers::

    transactions = [[1, 2, 5],
                    [2, 4],
                    [2, 3],
                    [1, 2, 4],
                    [1, 3],
                    [2, 3],
                    [1, 3],
                    [1, 2, 3, 5],
                    [1, 2, 3]]

Use find_frequent_patterns to find patterns in baskets that occur over the support threshold::

    patterns = pyfpgrowth.find_frequent_patterns(transactions, 2)

Use generate_association_rules to find patterns that are associated with another with a certain minimum probability::

    rules = pyfpgrowth.generate_association_rules(patterns, 0.7)

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
