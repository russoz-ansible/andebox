Usage
=====

Basic Usage
-----------

The general usage pattern obtained by running ``andebox --help`` is:

.. include:: _generated/andebox_help.rst

See :doc:`actions` for available actions.

Shell Completion
----------------

``andebox`` provides tab completion for sub-commands and options via `typer <https://typer.tiangolo.com>`_ (which supports Bash, Zsh, Fish, and PowerShell).

To install completion for your current shell, run once:

.. code-block:: shell

   andebox --install-completion

Restart your shell (or source its configuration file) and tab completion will be active.

To inspect the generated script without installing it:

.. code-block:: shell

   andebox --show-completion

After setup, pressing ``<TAB>`` after ``andebox`` will show available sub-commands, and pressing ``<TAB>`` after a sub-command will show its options.
