nox-test
========

Overview
--------
This action runs ``ansible-test`` within ``nox``, enabling testing across multiple Ansible Core
and Python versions without requiring any ``noxfile.py`` in your collection.
All session definitions are encapsulated inside ``andebox`` itself.

Version Matrix
^^^^^^^^^^^^^^
``andebox`` maintains an internal matrix of valid ``ansible-core`` × Python version combinations.
The default run executes **one Python version per ansible-core version** (shown below).
All supported combinations can be targeted using ``--ansible-core`` and ``--python``.

.. include:: ../_generated/noxtest_matrix.rst

Parameters
----------
The following parameters are supported:

``--ansible-core`` / ``-a``
    Restrict the run to one or more specific ``ansible-core`` versions (e.g. ``2.19``, ``2.20``).
    May be repeated. When omitted, all versions in the matrix are eligible.

``--python`` / ``-p``
    Restrict the run to one or more specific Python versions (e.g. ``3.12``, ``3.13``).
    May be repeated. Only combinations present in the matrix are selected.

``--session`` / ``-s``
    Pass one or more nox session names directly, bypassing matrix filtering.
    Session names follow the pattern ``acX.YY-pZ.WW``
    (e.g. ``ac2.20-p3.14``).

``--list`` / ``-l``
    List all available nox sessions without running anything.

``--reuse-venv`` / ``-r``
    Reuse existing virtual environments (equivalent to ``nox --reuse-existing-virtualenvs``).

After these parameters, you **must** pass ``--`` followed by any parameters you
wish to pass to ``ansible-test``. The ``--`` separator is required: without it,
arguments like ``sanity`` or ``--docker`` are not forwarded to ``ansible-test``
inside the nox session. See examples below.

Dependencies
------------
- ``nox`` is installed as a dependency of ``andebox``.
- ``ansible-core`` and ``andebox`` are installed into each nox session automatically.

Usage Examples
--------------
.. code-block:: shell

    # Run sanity tests with defaults (one python per ansible-core)
    andebox nox-test -- sanity --docker default

    # Run only against ansible-core 2.19 and 2.20
    andebox nox-test --ansible-core 2.19 --ansible-core 2.20 -- sanity --docker default

    # Run only with Python 3.12
    andebox nox-test --python 3.12 -- sanity --docker default

    # Run a specific ansible-core + python combination
    andebox nox-test --ansible-core 2.19 --python 3.13 -- units --docker default

    # List all available sessions
    andebox nox-test --list

    # Reuse existing virtual environments
    andebox nox-test --reuse-venv -- sanity --docker default
