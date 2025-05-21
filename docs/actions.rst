Actions
=======

andebox provides several actions:

test
----

Runs `ansible-test` directly in your collection.

.. code-block:: bash

   andebox test -- sanity --docker default --test validate-modules plugins/modules/mymodule.py

tox-test
--------

Runs `ansible-test` inside tox environments for multiple Ansible versions.

.. code-block:: bash

   andebox tox-test -- sanity --docker default --test validate-modules plugins/modules/mymodule.py

yaml-doc
--------

Analyzes and reformats YAML documentation blocks in your plugins.

.. code-block:: bash

   andebox yaml-doc plugins/modules/mymodule.py

Options:
- ``--offenders``: Report style issues.
- ``--fix-offenders``: Fix style issues.
- ``--dry-run``: Do not modify files.

runtime
-------

Shows information from ``runtime.yml`` (redirects, deprecations, tombstones).

.. code-block:: bash

   andebox runtime --plugin-type modules gce_net

docsite
-------

Builds the collection documentation site using ``antsibull-docs``.

.. code-block:: bash

   andebox docsite --dest-dir .builtdocs

See the CLI help (`andebox --help`) for more.
