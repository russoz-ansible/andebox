vagrant
=======

Overview
--------
This action runs ``andebox test -- integration`` inside a Vagrant-managed VM,
enabling integration testing for more complex modules/services.

The VM is expected to be defined in a ``Vagrantfile`` in the current directory.
It will be created and started if it is not ready, but specific provisioning
is not verified or enforced by this action.
By default, the action will not destroy the VM after the test completes,
but that can be achieved with the ``--destroy`` parameter.

If the test must be executed as ``root`` inside the VM, you need to use the ``--sudo`` parameter.

Tests executed with ``andebox vagrant`` are inherently slow, as the VMs take a
while to start and even longer to be provisioned.
It is probably a good idea to use this action only for specific tests executed locally.
For CI/CD pipelines, it is recommended to provision VMs dynamically in your
favorite cloud provider, run a regular ``andebox test -- integration`` in them, and then destroy them.

Vagrantfile
^^^^^^^^^^^

Unlike the ``tox-test`` action, this action does not generate a ``Vagrantfile``.
Instead, it expects a valid ``Vagrantfile`` to be present in the current directory.
Full-fledged VMs are heavier, trickier to configure and maintain, and possbily
dependent on environmental conditions, so that setup work is left to the user.

That being said, the VMs defined in your ``Vagrantfile`` should:

- map the current directory to ``/vagrant`` inside the VM, excluding
  directories like ``.git``, ``.tox`` and ``.vagrant``. ``vagrant`` runs
  ``rsync`` to sync the files inside the VM, so large directories take long
  to copy and delay the start of the VM.
- have Python installed, at least the minimum version required by ``andebox``.
- have a virtual environment created to run ``andebox`` from, by default it
  should be created in ``/venv``, but if you choose to create it in a different
  location, you will need to specify it with the ``--venv`` parameter.
- have ``andebox`` and ``ansible-core`` installed in the virtual environment.
- allow the user ``vagrant`` to run commands in that virtual environment.

You can see an example here: :download:`Vagrantfile <../examples/Vagrantfile>`

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
- ``python-vagrant`` and ``fabric`` will have been installed as dependencies of ``andebox``.
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
