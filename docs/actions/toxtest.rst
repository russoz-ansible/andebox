tox-test
========

Overview
--------
This action runs ``ansible-test`` within ``tox``, enabling testing across multiple Ansible versions using isolated environments.

The ``tox`` configuration
^^^^^^^^^^^^^^^^^^^^^^^^^
This action generates a ``tox`` configuration file named ``.andebox-tox-test.ini`` in the current directory.
That file is not overwritten nor updated by ``andebox`` when it already exists.
If you need something not supported by the existing file, you will need to update it manually.
On the other hand, if you have not customized the file, you can safely delete it to regenerate it.

The tox environments are expected to:

* have some version of ``ansible-core``
* be able to run ``andebox`` - the generated file will allow ``andebox`` as an external command, so
  if it is available outside tox, it will be available inside the tox environments as well.

Parameters
----------
The following parameters are supported:

``--env``, ``-e``
    Tox environments to run the test in (for example ``ac216``, ``dev``).

``--list``, ``-l``
    List all tox environments (equivalent to ``tox -a``).

``--recreate``, ``-r``
    Force recreation of virtual environments (equivalent to ``tox -r``).

After these parameters, you will usually want to pass ``--`` and after that, any
parameters you wish to use with ``ansible-test``. See examples below.

Dependencies
------------
- ``tox`` will have been installed as a dependency of ``andebox``.
- ``ansible-core`` and ``andebox`` must be available in the tox environments.

Usage Examples
--------------
.. code-block:: shell

    andebox tox-test --e ac216,ac217 -- sanity --docker default plugins/modules/mymodule.py
    andebox tox-test --list
    andebox tox-test --recreate -- units --docker default

Known Issues
------------
- The generated ``.andebox-tox-test.ini`` is not overwritten if it already exists.
