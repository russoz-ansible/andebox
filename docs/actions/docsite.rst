docsite
=======

Overview
--------
This action builds the documentation site for an Ansible collection using ``antsibull-docs``.
It works **only in a COLLECTION context**.

Parameters
----------
The following parameters are supported:

``--dest-dir``, ``-d``
    Directory which should contain the docsite (required).

``--keep``, ``-k``
    Keep the temporary collection directory after execution.

``--open``, ``-o``
    Open the browser pointing to the main page after build.

Dependencies
------------
- ``antsibull-docs`` and ``sphinx`` will have been installed as dependencies of ``andebox``.

Usage Examples
--------------
.. code-block:: shell

   # Generate docsite in the destination directory
   andebox docsite --dest-dir /tmp/mycollection_docsite

   # Generate docsite and open it in the browser
   andebox docsite -d /tmp/mycollection_docsite -o
