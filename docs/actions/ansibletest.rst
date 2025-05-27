test
====

Overview
--------
This action allows you to run ``ansible-test`` directly at the root directory
of an Ansible collection repository, or at the root of the ``ansible``
project itself.

That is achieved by creating a temporary copy of the collection using the
structure required by ``ansible-test`` and running the actual command in that
copy.

Parameters
----------
The following parameters are supported:

``--keep``, ``-k``
   Keep the temporary directory after execution, useful for debugging test .

``--exclude-from-ignore``, ``-efi``, ``-ei``
   Filter out matching lines in ignore files.

``--skip-requirements``, ``-R``
   Skip installation of ``requirements.yml``.

``--galaxy-retry``
   Number of retries when failing to retrieve requirements from galaxy (default: 3).

``[sanity|units|integration]``
   Test type to run (required).

After these parameters, you will usually want to pass ``--`` and after that, any
parameters you wish to use with ``ansible-test``. See examples below.

Dependencies
------------

This action requires ``ansible-test``.

When testing ``ansible`` itself, the tool is part of the repository and no additional installation is needed.
When testing an Ansible collection, then ``ansible-core`` is expected to be installed in the environment where ``andebox`` is run.


Usage Examples
--------------

Here we have three examples of how to use the ``test`` action, recorded within the community.general collection:

Sanity test:

.. image:: ../images/term/sanity.gif
   :alt: sanity test

Unit test:

.. image:: ../images/term/units.gif
   :alt: unit test

Integration test:

.. image:: ../images/term/integration.gif
   :alt: integration test

Known Issues
------------
- No known issues at this time.
