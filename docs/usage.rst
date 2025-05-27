Usage
=====

Basic usage
-----------

As of andebox 1.2.x, the general usage pattern obtained by running ``andebox --help`` is:

.. code-block:: text

   usage: andebox [-h] [--version] [--collection COLLECTION] [--venv VENV]
                  test context docsite ignores runtime tox-test vagrant yaml-doc ...

   Ansible Developer (Tool)Box v1.2.2

   positional arguments:
     test context docsite ignores runtime tox-test vagrant yaml-doc
       test                runs ansible-test in a temporary environment
       context             returns information from running context
       docsite             builds collection docsite
       ignores             gathers stats on ignore*.txt file(s)
       runtime             returns information from runtime.yml
       tox-test            runs ansible-test within tox, for testing in multiple ansible versions
       vagrant             runs 'andebox test -- integration' within a VM managed with vagrant
       yaml-doc            analyze and/or reformat YAML documentation in plugins

   options:
     -h, --help            show this help message and exit
     --version             show program's version number and exit
     --collection COLLECTION, -c COLLECTION
                           fully qualified collection name (not necessary if a proper galaxy.yml file is available)
     --venv VENV, -V VENV  path to the virtual environment where andebox and ansible are installed

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
