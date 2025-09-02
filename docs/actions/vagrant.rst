vagrant
=======

Overview
--------
This action runs ``andebox test -- integration`` inside a Vagrant-managed VM,
enabling integration testing for more complex modules/services.

The VM must be defined in ``Vagrantfile`` in the current directory. See more details below.
The action executes ``vagrant up`` when starting,
but it does not destroy the VM unless the ``--destroy`` parameter is used.

If the test must be executed as ``root`` inside the VM, you need to use the ``--sudo`` parameter.

Tests executed with ``andebox vagrant`` are inherently slow, as the VMs take a
while to start and even longer to be provisioned.
It is probably a good idea to use this action only for local tests.

Vagrantfile
^^^^^^^^^^^

The ``Vagrantfile`` file is **not created automatically**.
The **MUST** be present in the current directory for this action to work.

The VMs defined in your ``Vagrantfile``:

- MUST map the current directory to ``/vagrant`` inside the VM, excluding
  directories like ``.git``, ``.tox`` and ``.vagrant``. ``vagrant`` runs
  ``rsync`` to sync the files inside the VM, so large directories take long
  to copy and delay the start of the VM.
- MUST have Python installed, at least the minimum version required by ``andebox``.
- MUST have a virtual environment created to run ``andebox`` from, by default its
  path is ``/venv``, but if you choose to create it in a different
  location, you can specify it with the ``--venv`` parameter.
- MUST have ``andebox`` and ``ansible-core`` installed in the virtual environment.
- MUST allow the user ``vagrant`` to run commands in that virtual environment.

You can see an example here: :download:`Vagrantfile sample<../examples/Vagrantfile>`.
Disclaimer: all the VMs in this Vagrantfile worked at some point in time, but
that configuration is not tested and there is no guarantee it works by the time you read this.
Use it as guidance, not as a working artifact.

Parameters
----------
The following parameters are supported:

``--name``, ``-n``
    Name of the Vagrant VM to use (default: ``default``).

``--sudo``, ``-s``
    Use ``sudo`` to run ``andebox`` inside the VM.

``--destroy``, ``-d``
    Destroy the VM after the test completes.

After these parameters, you will usually want to pass ``--`` and after that, any
parameters you wish to use with ``andebox test -- integration``. See examples below.

Dependencies
------------
- ``vagrant`` must be installed and available in the system PATH.
- A valid ``Vagrantfile`` must exist in the current directory.

Usage Examples
--------------
.. code-block:: shell

    andebox vagrant --name freebsd14 --sudo -- destructive/pipx -v
    andebox vagrant -n debian12 -- --allow-destructive pipx --color yes -v
    andebox vagrant -n ubuntu-noble -s -- snap -v

Known Issues
------------
- If the ``Vagrantfile`` is missing, the action will fail.
- Since Hashicorp changed its licensing policies, a number of contributors stopped
  updating the VM images ("boxes") in Vagrant Cloud, so some systems/versions
  might be harder to find or unavailable altogether.
- ``vagrant`` and/or Vagrant Cloud are likely to impose additional requirements
  before you can download the boxes, such as logging in or accepting terms of service.
