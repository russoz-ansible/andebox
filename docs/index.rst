.. andebox-index

Andebox Documentation
=====================

.. toctree::
   :maxdepth: 1
   :caption: Contents:
   :hidden:

   usage
   actions
   contributing
   changelog

Ansible Developer's (tool)Box (**andebox**) is a CLI tool to assist Ansible
developers by encapsulating common tasks, such as running `ansible-test`,
managing tox environments, and more.

Basic Usage
-----------

Some examples of how you can use andebox:

.. code-block:: shell

   # setup-less execution of test
   cd community.general && andebox test -- sanity plugins/modules/*.py

   # reformat YAML doc blocks
   andebox yaml-doc plugins/modules/xfconf.py

   # generate HTML documentation for the collection
   andebox docsite -d /tmp/community_general_html

   # run integration test within vagrant VM
   andebox vagrant -n ubuntu-noble -s -- snap -v

See more details in the :doc:`usage` section, and in the corresponding sections for each one of the available actions.

Installation
------------

You can install andebox using ``pip``:

.. code-block:: shell

   pip install andebox

Or if you are using ``pipx`` (recommended!), do:

.. code-block:: shell

   pipx install andebox

The Secret
----------

For the actions that require a specfic directory structure, ``andebox`` creates a temporary copy of the project.
Because the actual commands are executed against a copy, ``andebox`` is free to support features that would otherwise
not be possible, modifying files temporarily.

When debugging your collection, some of the actions, notabaly ``test``, can be run with the ``--keep`` option,
which will keep the temporary directory after execution.
