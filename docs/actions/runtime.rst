runtime
=======

Overview
--------
This action returns information from the ``meta/runtime.yml`` file, such as plugin redirects, deprecations, and tombstones.
It works **only in a COLLECTION context**.

Parameters
----------
The following parameters are supported:

``--plugin-type``, ``-pt``
    Specify the plugin type to be searched (choices: connection, lookup, modules, doc_fragments, module_utils, callback, inventory).

``--regex``, ``--regexp``, ``-r``
    Treat plugin names as regular expressions.

``--info-type``, ``-it``
    Restrict type of response elements. Must be one of ``redirect``, ``tombstone``, or ``deprecation`` (can be shortened to one letter).

``plugin_names``
    One or more plugin names to query (required).

Dependencies
------------
- ``PyYAML`` will have been installed as a dependency of ``andebox``.

Usage Examples
--------------
.. code-block:: shell

    andebox runtime --plugin-type modules mymodule
    andebox runtime --plugin-type callback --regex '^osx_.*'
    andebox runtime --info-type d proxmox_disk
