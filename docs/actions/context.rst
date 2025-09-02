context
=======

Overview
--------
This action displays information about the context in which ``andebox`` is currently operating.
It is purely informational and helps in understanding how ``andebox`` perceives the current directory.

Parameters
----------
This action does not take any specific parameters.

Usage Examples
--------------

To display the current execution context for a collection (community.general in this example):

.. code-block:: shell

   $ andebox context
               Base dir: /home/user/git/community.general
                   Type: ContextType.COLLECTION
               Temp dir: /tmp/andebox.g_gsbod_
           ansible-test: ansible-test
           Sanity tests: tests/sanity
      Integration tests: tests/integration
             Collection: community.general 11.0.0

To display the current execution context for ``ansible-core``:

.. code-block:: shell

   $ andebox context
               Base dir: /home/user/git/ansible
                   Type: ContextType.ANSIBLE_CORE
               Temp dir: /tmp/andebox.ryph4pj4
           ansible-test: /tmp/andebox.ryph4pj4/bin/ansible-test
           Sanity tests: test/sanity
      Integration tests: test/integration

Or, if the directory is not recognized by ``andebox``:

.. code-block:: shell

   $ andebox context
   Cannot determine context for: /home/user/Desktop

In this last case, the command will return an exist staus of 1, indicating failure.
