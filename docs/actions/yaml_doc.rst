yaml-doc
========

Overview
--------
This action rewrites the YAML documentation blocks using consistent YAML formatting.
Additionally, it can report or fix potential style issues in the YAML content.

Please note that the ``EXAMPLES`` section of the YAML documentation may contains multiple
YAML documents, delimited with the ``---`` marker. In those cases, the action will
not process the content of the section, keeping it unchanged.

Parameters
----------
The following parameters are supported:

``--offenders``, ``-o``
    Report potential style-related offending constructs.

``--fix-offenders``, ``-O``
    Fix potential style-related offending constructs (implies ``--offenders``).

``--dry-run``, ``-n``
    Do not modify files (dry run mode).

``--width``, ``-w``
    Width for the YAML output (default: 120).

``--indent``, ``-i``
    Indentation for the YAML output (default: 2).

``files``
    Files where to search for YAML content (one or more required).

Dependencies
------------
- ``ruamel.yaml`` will have been installed as dependencies of ``andebox``.

Usage Examples
--------------
.. code-block:: shell

    andebox yaml-doc --offenders plugins/modules/mymodule.py
    andebox yaml-doc --fix-offenders --width 100 plugins/modules/mymodule.py
    andebox yaml-doc --dry-run plugins/modules/mymodule.py

Known Issues
------------
- Style rules are hardcoded and may not cover all possible cases.
- Rules are based in text search and may eventually produce false positives.
- Some style rules may be subjective or evolving.
