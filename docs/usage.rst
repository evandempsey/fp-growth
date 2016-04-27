=====
Usage
=====

To use FP-Growth in a project::

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

The FP-Growth algorithm uses a recursive implementation, so it is possible that if you feed a large transation set
into find_frequent_patterns you will see a 'maximum recursion depth exceeded' error. If you do, you can modify your recursion limit::

    import sys
    sys.setrecursionlimit(some_value)
