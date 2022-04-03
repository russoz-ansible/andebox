andebox
=======

Ansible Developer's (tool)Box, **andebox**, is a script to assist Ansible developers
by encapsulating some boilerplate tasks. One of the core features is the ability to run
`ansible-test` on a local copy of a collection repository without having to worry about
setting environment variables nor having the _expected_ directory structure _above_ the
collection directory.

It also allows some basic stats gathering from the `tests/sanity/ignore-X.Y.txt` files.

## Installation

Install it as usual:

    pip install andebox

### Dependencies

As of this version, the dependencies are `PyYAML` for reading `galaxy.yml`, and `ansible-core` itself
for running `ansible-test`.

## Usage

After installing the tool (ensuring it is reachable in from `PATH`), there are different actions available, as described below.

### Simplify ansible-test

No need to clone in specific locations or keep track of env variables. Simply clone whichever collection you want and
run the `ansible-test` command as:

```bash
$ andebox test -- sanity --docker default --test validate-modules plugins/modules/mymodule.py
$ andebox test -- unit --docker default test/units/plugins/modules/mymodule.py
$ andebox test -- integration --docker default mymodule
```

By default, `andebox` will discover the full name of the collection by parsing the `galaxy.yml` file usually found in
the local directory.
If the file is not present or if it fails for any reason, the option `--collection` may be used to specify it, as in:

```bash
$ andebox test --collection community.general -- sanity --docker default -v --test validate-modules
```

Please notice that `andebox` uses whichever `ansible-test` is available in `PATH` for execution

### Multiple ansible-test

Simply run one of :

```bash
$ andebox tox-test -- sanity --docker default --test validate-modules plugins/modules/mymodule.py
$ andebox tox-test -- unit --docker default test/units/plugins/modules/mymodule.py
$ andebox tox-test -- integration --docker default mymodule
```

Or specify the ansible versions you want tested:

The `tox-test` will create a custom `tox.ini` file with the name `.andebox-tox-test.ini` in the current directory.
That file will not be overwritten by `andebox`, and by default it will provide the following tox environments:

    envlist = 29, 210, 211, 212, a3, a4, a5, dev

You can run the test on all of them by default, or specify which ones to use, like:

```bash
$ andebox tox-test -e 29 -- sanity --docker default --test validate-modules plugins/modules/mymodule.py
$ andebox tox-test -e 211,212 -- unit --docker default test/units/plugins/modules/mymodule.py
$ andebox tox-test -e a4,dev -- integration --docker default mymodule
```

### Stats on ignore files

Gathering stats from the ignore files can be quite annoying, especially if they are long. One can run:

```bash
$ andebox ignores -v2.10 -d4 -fc '.*:parameter-list-no-elements'
    24  plugins/modules/cloud/ovirt validate-modules:parameter-list-no-elements
     8  plugins/modules/cloud/centurylink validate-modules:parameter-list-no-elements
     6  plugins/modules/remote_management/redfish validate-modules:parameter-list-no-elements
     5  plugins/modules/cloud/oneandone validate-modules:parameter-list-no-elements
     4  plugins/modules/cloud/rackspace validate-modules:parameter-list-no-elements
     4  plugins/modules/remote_management/oneview validate-modules:parameter-list-no-elements
     3  plugins/modules/cloud/opennebula validate-modules:parameter-list-no-elements
     3  plugins/modules/cloud/univention validate-modules:parameter-list-no-elements
     3  plugins/modules/clustering/consul validate-modules:parameter-list-no-elements
     3  plugins/modules/monitoring/sensu validate-modules:parameter-list-no-elements
```

### Runtime config

Quickly peek what is the `runtime.yml` status for a specific module:

```bash
$ andebox runtime scaleway_ip_facts
D modules scaleway_ip_facts: deprecation in 3.0.0 (current=2.4.0): Use community.general.scaleway_ip_info instead.
```

Or using a regular expression:

```bash
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
