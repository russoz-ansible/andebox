Actions
=======

.. toctree::
   :hidden:

   actions/context
   actions/docsite
   actions/ignorefile
   actions/runtime
   actions/ansibletest
   actions/toxtest
   actions/vagrant
   actions/yaml_doc

``andebox`` provides these actions to be executed:

:doc:`actions/context`
   This action is merely informative and will show the execution context detected by ``andebox``.

:doc:`actions/docsite`
   This action allows you to build the collection documentation site using ``antsibull-docs``, straight from the collection directory, no setup needed.

:doc:`actions/ignorefile`
   This action consolidates occurrences of sanity tests exemptions from the ``<test or tests>/sanity/ignore*.txt`` files.

:doc:`actions/runtime`
   This action shows information from the ``meta/runtime.yml`` (redirects, deprecations, tombstones).

:doc:`actions/ansibletest`
   This action allows you to run ``ansible-test``, for sanity, unit, or integration tests, straight from the collection directory, no setup needed.

:doc:`actions/toxtest`
   This action allows you to run ``ansible-test``, just like the ``test`` action, but testing in different ``tox`` environments.
   By using this action you can run your test in multiple versions of Ansible, with just one command.

:doc:`actions/vagrant`
   Some integration tests require more complicated and sometimes heavier setups, making them more suitable to be executed in virtual machines.
   For those cases, it is interesting to leverage ``vagrant`` to easily create, provision, and destroy these environments, and
   the ``vagrant`` action enables you to use Vagrant VMs to smoothly run those tests.

:doc:`actions/yaml_doc`
   You can use this action to reformat the YAML documentation blocks in your plugins, and also to pick on some style issues.


See the CLI help (``andebox --help``) for more.
