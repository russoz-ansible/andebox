ignores
=======

Overview
--------
This action gathers statistics on ``ignore*.txt`` files used by sanity tests.
It summarizes ignored checks and files.

Parameters
----------
The following parameters are supported:

``--spec SPEC``, ``-s SPEC``
    Use ``ignore-SPEC.txt``, or pass ``-`` to read from stdin.

``--depth``, ``-d``
    Path depth for grouping files.
    For example, with a depth of 2, the result will show the count of
    occurrences for ``plugins/modules``, ``plugins/module_utils``, etc, instead
    of the full paths like ``plugins/modules/mymodule.py``.
    This is useful for large collections with modules files organized
    hierarchically.

``--filter-files``, ``-ff``
    Regular expression matching file names to be included.

``--filter-checks``, ``-fc``
    Regular expression matching checks in ignore files to be included.

``--suppress-files``, ``-sf``
    Suppress file names from the output, consolidating the results.

``--suppress-checks``, ``-sc``
    Suppress the checks from the output, consolidating the results.

``--head``, ``-H``
    Number of lines to display in the output: leading lines if positive, trailing lines if negative, all lines if zero (default: 10).

Dependencies
------------
No special dependencies.

Usage Examples
--------------
.. code-block:: shell

    andebox ignores --spec 2.16
    andebox ignores --filter-files test_module
    andebox ignores --head 5

Known Issues
------------
- No known issues at this time.
