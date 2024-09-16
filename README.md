andebox
=======

Ansible Developer's (tool)Box, **andebox**, is a script to assist Ansible developers
by encapsulating some boilerplate tasks. One of the core features is the ability to run
`ansible-test` on a local copy of a collection repository without having to worry about
setting environment variables nor having the _expected_ directory structure _above_ the
collection directory.

It also allows some basic stats gathering from the `tests/sanity/ignore-X.Y.txt` files.

Installation
------------

Install it as usual:

    pip install andebox

Requirements
------------

* ansible-core for actions `test` and `tox-test`
* pyyaml for reading galaxy.yml
* distutils for comparing `LooseVersion` objects for action `ignore`
* vagrant for action `vagrant`
  * `andebox` and any other dependency must be installed inside the VM, but that setup is the user responsibility

Setup-less ansible-test
-----------------------

No need to clone in specific locations or keep track of env variables. Simply clone whichever collection you want and
run the `ansible-test` command as:

```
# Run sanity test(s)
$ andebox test -- sanity --docker default --test validate-modules plugins/modules/mymodule.py

# Run sanity test(s) excluding the modules listed in the CLI from the sanity 'ignore-X.Y.txt' files
$ andebox test -ei -- sanity --docker default --test validate-modules plugins/modules/mymodule.py

# Run unit test(s)
$ andebox test -- unit --docker default test/units/plugins/modules/mymodule.py

# Run integration test
$ andebox test -- integration --docker default mymodule

# Run tests in multiple Ansible versions using tox
$ andebox tox-test -- sanity --docker default --test validate-modules plugins/modules/mymodule.py
$ andebox tox-test -- unit --docker default test/units/plugins/modules/mymodule.py
$ andebox tox-test -- integration --docker default mymodule

# Run tests in multiple specific Ansible versions using tox
$ andebox tox-test -e ac211,ac212 -- unit --docker default test/units/plugins/modules/mymodule.py     # ansible-core 2.11 & 2.12 only
$ andebox tox-test -e a4,dev -- integration --docker default mymodule                                 # ansible 4 & development branch
```

By default, `andebox` will discover the full name of the collection by parsing the `galaxy.yml` file found in
the local directory.
If the file is not present or if it fails for any reason, use the option `--collection` to specify it, as in:

```
$ andebox test --collection community.general -- sanity --docker default -v --test validate-modules
```

Please notice that `andebox` uses whichever `ansible-test` is available in `PATH` for execution

Stats on ignore files
---------------------

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

Runtime config
--------------

Quickly peek what is the `runtime.yml` status for a specific module:

```
$ andebox runtime scaleway_ip_facts
D modules scaleway_ip_facts: deprecation in 3.0.0 (current=2.4.0): Use community.general.scaleway_ip_info instead.
```

Or using a regular expression:

```
$ andebox runtime -r 'gc[pe]'
R lookup gcp_storage_file: redirected to community.google.gcp_storage_file
T modules gce: terminated in 2.0.0: Use google.cloud.gcp_compute_instance instead.
R modules gce_eip: redirected to community.google.gce_eip
R modules gce_img: redirected to community.google.gce_img
R modules gce_instance_template: redirected to community.google.gce_instance_template
R modules gce_labels: redirected to community.google.gce_labels
R modules gce_lb: redirected to community.google.gce_lb
R modules gce_mig: redirected to community.google.gce_mig
R modules gce_net: redirected to community.google.gce_net
R modules gce_pd: redirected to community.google.gce_pd
R modules gce_snapshot: redirected to community.google.gce_snapshot
R modules gce_tag: redirected to community.google.gce_tag
T modules gcp_backend_service: terminated in 2.0.0: Use google.cloud.gcp_compute_backend_service instead.
T modules gcp_forwarding_rule: terminated in 2.0.0: Use google.cloud.gcp_compute_forwarding_rule or google.cloud.gcp_compute_global_forwarding_rule instead.
T modules gcp_healthcheck: terminated in 2.0.0: Use google.cloud.gcp_compute_health_check, google.cloud.gcp_compute_http_health_check or google.cloud.gcp_compute_https_health_check instead.
T modules gcp_target_proxy: terminated in 2.0.0: Use google.cloud.gcp_compute_target_http_proxy instead.
T modules gcp_url_map: terminated in 2.0.0: Use google.cloud.gcp_compute_url_map instead.
R modules gcpubsub: redirected to community.google.gcpubsub
R modules gcpubsub_info: redirected to community.google.gcpubsub_info
R modules gcpubsub_facts: redirected to community.google.gcpubsub_info
R doc_fragments _gcp: redirected to community.google._gcp
R module_utils gce: redirected to community.google.gce
R module_utils gcp: redirected to community.google.gcp
```
where D=Deprecated, T=Tombstone, R=Redirect.

Run Integration Tests in Vagrant VMs
------------------------------------

To run the test inside a VM managed by [vagrant](https://www.vagrantup.com/):

```
# Run test in VM named "fedora37" using sudo
$ andebox vagrant -n fedora37 -s -- --python 3.9 xfs_quota --color yes
```

Also beware that `andebox` does not create nor manage `Vagrantfile`. The user is responsible for creating and setting up the VM definition. It must have `andebox` and `ansible-core` (or `ansible-base` or `ansible`) installed on a virtual environment. By default, the venv is expected to be at `/venv` but the location can be specified using the `--venv` parameter.
