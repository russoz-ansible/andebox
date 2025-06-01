andebox
=======

[![PyPI - Version](https://img.shields.io/pypi/v/andebox.svg)](https://pypi.org/project/andebox/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/andebox)
![PyPI - Downloads](https://img.shields.io/pypi/dw/andebox)
[![Last Commit](https://img.shields.io/github/last-commit/russoz-ansible/andebox)](https://github.com/russoz-ansible/andebox/commits/main)

[![Build Status](https://github.com/russoz-ansible/andebox/actions/workflows/ci-tests.yml/badge.svg?branch=)](https://github.com/russoz-ansible/andebox/actions)
[![docs](https://readthedocs.org/projects/andebox/badge/?style=flat)](https://andebox.readthedocs.io/en/latest/)
[![codecov](https://codecov.io/gh/russoz-ansible/andebox/graph/badge.svg?token=D3TPI2PGU9)](https://codecov.io/gh/russoz-ansible/andebox)

**andebox** is a script to assist Ansible developers by encapsulating some
boilerplate tasks, especially the ability of running tests from the root
directory of the collection project without any additional setup.

![andebox integration test demo](https://raw.githubusercontent.com/russoz-ansible/andebox/main/docs/images/term/integration.gif)

Highlights
----------

### Setup-less ansible-test

No need to clone in specific locations or keep track of env variables. Simply clone whichever collection you want and
run the `ansible-test` command as:

```
$ andebox test -- sanity --docker default --test validate-modules plugins/modules/mymodule.py
$ andebox test -- unit --docker default test/units/plugins/modules/mymodule.py
$ andebox test -- integration --docker default mymodule
```

If you want to test your code against multiple versions of `ansible-core` or other component, you
will like the `tox-test` subcommand as well.

### Stats on ignore files

Gathering stats from the ignore files can be quite annoying, especially if they are long. One can run:

```
$ andebox ignores -v2.10 -d4 -fc '.*:parameter-list-no-elements'
    24  plugins/modules/ovirt validate-modules:parameter-list-no-elements
     8  plugins/modules/centurylink validate-modules:parameter-list-no-elements
     6  plugins/modules/redfish validate-modules:parameter-list-no-elements
     5  plugins/modules/oneandone validate-modules:parameter-list-no-elements
     4  plugins/modules/rackspace validate-modules:parameter-list-no-elements
     4  plugins/modules/oneview validate-modules:parameter-list-no-elements
     3  plugins/modules/opennebula validate-modules:parameter-list-no-elements
     3  plugins/modules/univention validate-modules:parameter-list-no-elements
     3  plugins/modules/consul validate-modules:parameter-list-no-elements
     3  plugins/modules/sensu validate-modules:parameter-list-no-elements
```

### Runtime config

Quickly peek what is the `runtime.yml` status for a specific module:

```
$ andebox runtime scaleway_ip_facts
D modules scaleway_ip_facts: deprecation in 3.0.0 (current=2.4.0): Use community.general.scaleway_ip_info instead.
```

Or using a regular expression:

```
$ andebox runtime -r 'gc[pe]' | head -5
R lookup gcp_storage_file: redirected to community.google.gcp_storage_file
T modules gce: terminated in 2.0.0: Use google.cloud.gcp_compute_instance instead.
R modules gce_eip: redirected to community.google.gce_eip
R modules gce_img: redirected to community.google.gce_img
R modules gce_instance_template: redirected to community.google.gce_instance_template
```
where D=Deprecated, T=Tombstone, R=Redirect.

### Run Integration Tests in Vagrant VMs

To run integration tests inside a VM managed by [vagrant](https://www.vagrantup.com/):

```
# Run test in VM named "fedora37" using sudo
$ andebox vagrant -n fedora37 -s -- --python 3.9 xfs_quota --color yes
```

`andebox` does not manage your `Vagrantfile`. The user is responsible for creating and setting up the VM definition.

Installation
------------

Install it as usual:

    pip install andebox
