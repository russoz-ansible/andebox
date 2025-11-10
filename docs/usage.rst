Usage
=====

Basic usage
-----------

The general usage pattern obtained by running ``andebox --help`` is:

.. include:: _generated/andebox_help.rst

See :doc:`actions` for available actions.

Shell Completion (argcomplete)
------------------------------

``andebox`` uses the ``argcomplete`` library to provide command-line argument completion (also known as tab completion).

To enable shell completion, you need to run a command once or add a line to your shell's configuration file.

**Enabling Completion:**

The recommended way to enable completion is by running the activation script. Open your terminal and execute:

.. code-block:: shell

   activate-global-python-argcomplete

This command will attempt to update the configuration for your detected shell. You may need to restart your shell or source its configuration file for the changes to take effect.

**Shell-Specific Instructions:**

If the activation script doesn't work or you prefer manual setup, here are common instructions:

*   **Bash:** Add the following to your ``~/.bashrc`` (or ``~/.bash_profile`` on macOS):

    .. code-block:: shell

       eval "$(register-python-argcomplete --shell bash)"

    Then source the file (e.g., ``source ~/.bashrc``) or open a new terminal.

*   **Zsh:** Add the following to your ``~/.zshrc``:

    .. code-block:: shell

       autoload -U compinit && compinit
       eval "$(register-python-argcomplete --shell zsh)"

    Then source the file (e.g., ``source ~/.zshrc``) or open a new terminal.

*   **Tcsh:** Add the following to your ``~/.tcshrc``:

    .. code-block:: shell

       eval `register-python-argcomplete --shell tcsh`

    Then source the file (e.g., ``source ~/.tcshrc``) or open a new terminal.

*   **Fish:** Create a completion file:

    .. code-block:: shell

       register-python-argcomplete --shell fish > ~/.config/fish/completions/python-argcomplete.fish

    Then open a new terminal.

After setting up completion for your shell, you should be able to type ``andebox``, press ``<TAB>``, and see available sub-commands. Typing a sub-command and then ``<TAB>`` should show its options.

For more detailed information on setting up ``argcomplete``, please refer to the `argcomplete documentation <https://kislyuk.github.io/argcomplete/>`_.
