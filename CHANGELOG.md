# CHANGELOG


## v0.98.1 (2025-05-31)

### Bug Fixes

- **action/ignores**: Add missing `f` to f-strings
  ([`241616c`](https://github.com/russoz-ansible/andebox/commit/241616cae5a2e3ca602e4ac15f6ce46e8388738c))

### Chores

- Add modelines to files
  ([`6121cb7`](https://github.com/russoz-ansible/andebox/commit/6121cb7cdd8df5c994374c4c77f20ada62d7906f))

- Update .pre-commit-config.yaml
  ([`4261993`](https://github.com/russoz-ansible/andebox/commit/42619934c9bb866c4d631bdbbb1f416d628f26c3))

- **devcontainer**: Fix structure, add vscode plugins
  ([`cb8d55f`](https://github.com/russoz-ansible/andebox/commit/cb8d55f8c4303a655338767b072bae671a9778fe))

- **TODO**: Pre-commit updates
  ([`cb4ccfa`](https://github.com/russoz-ansible/andebox/commit/cb4ccfa4daae6e29ebab8193bcfe5e4c280db322))

### Continuous Integration

- **codecov**: Add codecov.yml (again)
  ([`a6df881`](https://github.com/russoz-ansible/andebox/commit/a6df881fd39c09493959b65c8767db00cd3b3d1e))

- **codecov**: Lower coverage target for now
  ([`c961156`](https://github.com/russoz-ansible/andebox/commit/c96115601abf4c020520dd634abe3de56ec2090f))

### Documentation

- Revamp TODO.md
  ([`8c33bbe`](https://github.com/russoz-ansible/andebox/commit/8c33bbe7b8203f625c475ee92237b0d05d882613))

- **ascii-demo**: Fix URL for integration demo
  ([`f4a09dd`](https://github.com/russoz-ansible/andebox/commit/f4a09dd93a7306e5986a7b5dd65aca92b882a0c0))

### Refactoring

- **test_action_ansibletest**: Rename function
  ([`ad09bc9`](https://github.com/russoz-ansible/andebox/commit/ad09bc99b9abc2ff126b740953dee74cb81f2d3b))

- **tests**: Move constans with repo URLs to utils
  ([`18da888`](https://github.com/russoz-ansible/andebox/commit/18da88855326acc001e1fbdcd33b8c404134c807))

### Testing

- **coverage**: Add definition for excluded lines
  ([`906f5db`](https://github.com/russoz-ansible/andebox/commit/906f5db8dc97f17a7406af5a3bf130396b27d8ae))

- **ignores**: Add initial testcase
  ([`1935510`](https://github.com/russoz-ansible/andebox/commit/193551022998b49c700f811225977dba79ddb10d))


## v0.98.0 (2025-05-30)

### Chores

- Remove unused MANIFEST.in
  ([`64fee42`](https://github.com/russoz-ansible/andebox/commit/64fee42a1b2f218dfda8420b255088108b026026))

- Review license headers
  ([`02cc52a`](https://github.com/russoz-ansible/andebox/commit/02cc52a7d922e46a8940f2db0040f86c69492402))

### Continuous Integration

- **codecov**: Add config, prevent codecov from blocking CI
  ([`098f33c`](https://github.com/russoz-ansible/andebox/commit/098f33ca2e68abaadbec0e808ebf54f57380b9aa))

### Documentation

- Add TODO.md
  ([`a964e7a`](https://github.com/russoz-ansible/andebox/commit/a964e7aac60c25966df0870613248cd1077ce15c))

- **ascii-demo**: Add ability to generate ascii demos
  ([`50e492e`](https://github.com/russoz-ansible/andebox/commit/50e492efee787d101cb90f046cf1fb7a989ada5b))

- **ascii-demo**: Improve setup of dependencies
  ([`8b7231e`](https://github.com/russoz-ansible/andebox/commit/8b7231e3f413b1350e652ca946f11d9321c6f964))

- **readme**: Adjust badges
  ([`92fbdce`](https://github.com/russoz-ansible/andebox/commit/92fbdce6973e59760ae165198a7d778c0e44380b))

- **readme**: Adjust text order and headings
  ([`9096b6d`](https://github.com/russoz-ansible/andebox/commit/9096b6d94d2aa16b5104e55897032c80010f544f))

### Features

- Add module execution protocol
  ([`715bd74`](https://github.com/russoz-ansible/andebox/commit/715bd742482e8e6e73411eb892ab43ba3b067f1e))

### Refactoring

- Rename module from andeboxlib to andebox
  ([`735967e`](https://github.com/russoz-ansible/andebox/commit/735967ee1985c83156704a39cc6b390a8646e324))


## v0.97.0 (2025-05-30)

### Documentation

- **readme**: Add badges
  ([`c3a0934`](https://github.com/russoz-ansible/andebox/commit/c3a0934b5d227d0b6fb6f2ce6184c0caa73f9e31))

- **readme**: Fix github test badge
  ([`f1816c1`](https://github.com/russoz-ansible/andebox/commit/f1816c146c860ab628c77694ee16eaf0e76fa0a9))

- **readme**: More badges
  ([`4eaead2`](https://github.com/russoz-ansible/andebox/commit/4eaead2b95daf7ff3dbbb531ff4f25b9ca3552a3))

### Features

- Change dev status from alpha to beta
  ([`a1be7a0`](https://github.com/russoz-ansible/andebox/commit/a1be7a02b8f7d54bc6d898e4524a52d3feedf228))

- **ansible-test**: Add retry logic to requirements install
  ([`18ee1ae`](https://github.com/russoz-ansible/andebox/commit/18ee1ae49b7667f65a5933c90506d84bb8fe8921))

### Refactoring

- Add type hints/annotations
  ([`40c7b62`](https://github.com/russoz-ansible/andebox/commit/40c7b62a07c54c949084edd924a143eed2cf35c3))

- Move load_module_vars() in tests/test_action_yaml_doc.py
  ([`c096378`](https://github.com/russoz-ansible/andebox/commit/c096378104f7fd650879f295fd0de00d7e255faa))

For readability

- **tests**: Change testcase field from `output` to `expected`
  ([`6032251`](https://github.com/russoz-ansible/andebox/commit/603225177fe5e0dfd3303d0d438240628edd10fe))

### Testing

- Create class AndeboxTestHelper
  ([`3598622`](https://github.com/russoz-ansible/andebox/commit/359862222898b3dad6946dc359c15b83d465ac2a))

Refactored out of existing tests

- Revamp of AndeboxTestHelper
  ([`3ef9b32`](https://github.com/russoz-ansible/andebox/commit/3ef9b326094bbe9a40d8c2320e4df0a5cc4e7a55))

* Streamline the logic and the separation of concerns between the test files and the helper code. *
  Add a number of minor improvements.

- **action/ansibletest**: Use AndeboxTestHelper
  ([`de27943`](https://github.com/russoz-ansible/andebox/commit/de2794362ea61f9797d96e111e79aa45d8640d95))

- **action/context**: Use AndeboxTestHelper
  ([`cf32b95`](https://github.com/russoz-ansible/andebox/commit/cf32b9571f29fadea086a3292605c813f73b6232))

- **action/yaml-doc**: Use AndeboxTestHelper
  ([`7674f1e`](https://github.com/russoz-ansible/andebox/commit/7674f1e67831bb6c87915565c2e78a3375562725))

- **reports**: Add junit-style and coverage report
  ([`7a33e9d`](https://github.com/russoz-ansible/andebox/commit/7a33e9d8504cc49a15df21ab666f018933b6f46d))

- **yaml tests**: Make `exception` a top-level field
  ([`21b3a31`](https://github.com/russoz-ansible/andebox/commit/21b3a31bfa8d45b0645cd83551dda37129731167))


## v0.96.0 (2025-05-27)

### Features

- Install requirements by default
  ([`90d3fcf`](https://github.com/russoz-ansible/andebox/commit/90d3fcf80fb5583fc203e28b4c4d15058d72ea5d))

When running unit or integration tests, install the Ansible dependencies defined in the
  corresponding `requirements.yml` file. The semantics of the `-R` parameter has been inverted, and
  its long form has been renamed to `--skip-requirements`. As the suggests, when passed, that option
  skips the installation of those requirements.

The `vagrant` action is affected - requirements should be installed when running andebox inside the
  VM, so the `-R` has been removed from that execution.


## v0.95.1 (2025-05-27)

### Bug Fixes

- **context**: Handle invalid repos correctly
  ([`d201cd8`](https://github.com/russoz-ansible/andebox/commit/d201cd8da5382423e6587b4db30911705e15f9d2))

### Chores

- Add AI prompt
  ([`e178698`](https://github.com/russoz-ansible/andebox/commit/e17869894c6dede13196ab27be526b62b74739e7))

- **ai-prompt**: Refine python persona
  ([`d6b2802`](https://github.com/russoz-ansible/andebox/commit/d6b2802ae43b6cd18f9d616ac60a302f459e9001))

- **ai-prompt**: Refine python persona
  ([`e0f2002`](https://github.com/russoz-ansible/andebox/commit/e0f2002a353553dcd51a29b353220a7278670755))

- **devcontainer**: Configure ssh agent inside container
  ([`7441507`](https://github.com/russoz-ansible/andebox/commit/74415070a998e781c217f6fa8a9dba0c4c267977))

### Documentation

- Minor improvement in README
  ([`e3f0b26`](https://github.com/russoz-ansible/andebox/commit/e3f0b262eb0defa933a911da2d4b334328b733d6))

- **test/utils**: Reduce verbose comment
  ([`8f24dc3`](https://github.com/russoz-ansible/andebox/commit/8f24dc330e08400fab9a808209de6ab9b7d2ba48))

### Refactoring

- Simplify dependency handling code
  ([`f4bb584`](https://github.com/russoz-ansible/andebox/commit/f4bb584dcedcdc7fbf2148d9693286bf1c1d2584))

- **test_action_ansibletest**: Improve the handling of `skip_py`
  ([`beaf804`](https://github.com/russoz-ansible/andebox/commit/beaf8047930ad7ba1adc0d5db70eb778dd75c429))

### Testing

- Create fixture run_andebox
  ([`b0323e9`](https://github.com/russoz-ansible/andebox/commit/b0323e94915c2a42085fb1aeaf5f097efc4bd643))

- Remove unused MockContext dataclass
  ([`7065f99`](https://github.com/russoz-ansible/andebox/commit/7065f99ac82b53a61153d75f5218fd1b735a20f0))

- **ansibletest**: Define testcases in yaml
  ([`58f1b4c`](https://github.com/russoz-ansible/andebox/commit/58f1b4ccf576f27e7f76eb8e48f37da9cf92c365))

- **ansibletest**: Test within python, no subprocess
  ([`a16ff56`](https://github.com/russoz-ansible/andebox/commit/a16ff56fc1af7b8a837b43cbd92ddcf4f30fe025))

- **context**: Test within python, no subprocess
  ([`6bafbb0`](https://github.com/russoz-ansible/andebox/commit/6bafbb0162f7909cb1eb16d332a178aca4779e84))

- **yaml-doc**: Use fixture run_andebox
  ([`f5fb1f8`](https://github.com/russoz-ansible/andebox/commit/f5fb1f8973edd9c1ff249f286972bbb32b4b093a))


## v0.95.0 (2025-05-26)

### Bug Fixes

- **yaml_doc**: Re-add the exception raised if ruamel.yaml not present
  ([`efa9f23`](https://github.com/russoz-ansible/andebox/commit/efa9f239045331d41d511cd8a49c3785ced0bf46))

### Code Style

- **yaml_doc**: Remove redundant comments
  ([`47f897b`](https://github.com/russoz-ansible/andebox/commit/47f897bb7b96937f431b2734fc67d9d53244ee56))

### Features

- Improve dependecy handling in actions
  ([`32c6ab3`](https://github.com/russoz-ansible/andebox/commit/32c6ab3855e148a542fa32180dbfe98c01c56bb0))

In both `vagrant` and `yaml-doc` actions, dependency handling now does a better job in terms of good
  practices in code and informing hte user of the issue

### Refactoring

- **yaml_doc**: Remove redundant assert for json_samples
  ([`1078d17`](https://github.com/russoz-ansible/andebox/commit/1078d1755a97c64f9fff4534f95a4925471153cf))

- **yaml_doc**: Simplify _store_json_sample()
  ([`08e7319`](https://github.com/russoz-ansible/andebox/commit/08e73196491870af6c4f5eb2fc31fc333cc2a250))


## v0.94.2 (2025-05-25)

### Bug Fixes

- **yaml_doc**: Generate json `sample` as `dict`/`list`
  ([`5077b86`](https://github.com/russoz-ansible/andebox/commit/5077b866b01e8bf73509469629921f9fc98a4e01))

- **yaml_doc**: Use counter to generate unique sample id
  ([`b6001a4`](https://github.com/russoz-ansible/andebox/commit/b6001a4ec40b1e8bd6a2d1f5ed920138fcc52507))

Even when the contents are the same

### Testing

- Simplify fixture git_repo
  ([`45becfc`](https://github.com/russoz-ansible/andebox/commit/45becfc666c835f8ff74bbb058860d8489516594))

- **yaml_doc**: Mock collection directory
  ([`f95460c`](https://github.com/russoz-ansible/andebox/commit/f95460c2e3e8538f87a819118ed3644f2b63af59))


## v0.94.1 (2025-05-24)

### Bug Fixes

- **yaml_doc**: Remove start marker from first line
  ([`0b7c694`](https://github.com/russoz-ansible/andebox/commit/0b7c694c06151b71a06d6ffe8697c5770bca41b0))


## v0.94.0 (2025-05-22)

### Chores

- Publish only when there is a new semantic release
  ([#61](https://github.com/russoz-ansible/andebox/pull/61),
  [`b21947f`](https://github.com/russoz-ansible/andebox/commit/b21947ff785af64ab32fa506feb8a2ef2764a474))

### Features

- **readthedocs**: Adjust the config file ([#62](https://github.com/russoz-ansible/andebox/pull/62),
  [`a137a26`](https://github.com/russoz-ansible/andebox/commit/a137a26ae7d85b09cd5c6fec5ef9f3820b051db4))

### Testing

- Add test for tox docs ([#60](https://github.com/russoz-ansible/andebox/pull/60),
  [`19f54b1`](https://github.com/russoz-ansible/andebox/commit/19f54b1de2fc0ceebaad4a9111913b0f8bf0d688))


## v0.93.5 (2025-05-21)

### Bug Fixes

- Typo in pyproject for semantiv-release variables
  ([`43a28d9`](https://github.com/russoz-ansible/andebox/commit/43a28d9636c013b9854aac8df82dac198c53b4a3))


## v0.93.4 (2025-05-21)

### Bug Fixes

- Rollback semantic-release config for updating version vars
  ([`db6dd80`](https://github.com/russoz-ansible/andebox/commit/db6dd8008955852a3bc4cab68aaa09d0ae548a8c))


## v0.93.3 (2025-05-21)

### Bug Fixes

- Semantic-release config for updating version vars
  ([`09f420a`](https://github.com/russoz-ansible/andebox/commit/09f420a284c4ad432a5df2b108816d80ebd11ad3))


## v0.93.2 (2025-05-21)

### Bug Fixes

- Set pypi token env var again
  ([`07f5ed3`](https://github.com/russoz-ansible/andebox/commit/07f5ed3bf3106f61de7924ef0ff158021cb55525))


## v0.93.1 (2025-05-21)

### Bug Fixes

- Version numbers in docs/conf.py and cli.py
  ([`758714f`](https://github.com/russoz-ansible/andebox/commit/758714f59fa1ab9b3c9ff034bfb15416b266f69d))


## v0.93.0 (2025-05-21)

### Features

- **poetry-lock**: Refactor the lock command into test and release workflows
  ([`dabb449`](https://github.com/russoz-ansible/andebox/commit/dabb449d701163a1d5b8d25e3bd8840b9dd36029))

- **semantic-release**: Add poetry lock to the release workflow
  ([`d6e5618`](https://github.com/russoz-ansible/andebox/commit/d6e5618dfdfa3192f92f1d9ec92c4092b299cee5))

- **semantic-release**: Call poetry lock workflow
  ([`b110e0c`](https://github.com/russoz-ansible/andebox/commit/b110e0cc03321b203892dcc4deb0e6134b113765))

- **semantic-release**: Rename workflow file
  ([`4b52190`](https://github.com/russoz-ansible/andebox/commit/4b52190464068441e79a0e2f42479af57c8dc675))


## v0.92.4 (2025-05-21)

### Bug Fixes

- **semantic-release**: Trying again
  ([`a77bdb9`](https://github.com/russoz-ansible/andebox/commit/a77bdb9e7b0d4882361834672f89ddd6adfbb0d1))


## v0.92.3 (2025-05-21)

### Bug Fixes

- **semantic-release**: Trying again
  ([`a15845e`](https://github.com/russoz-ansible/andebox/commit/a15845e165769b2c111bbe09522345a8f046e029))


## v0.92.2 (2025-05-21)

### Bug Fixes

- **semantic-release**: Change token variable
  ([`329bec4`](https://github.com/russoz-ansible/andebox/commit/329bec451b930f57e4f15456e2acd41e5554eeb7))


## v0.92.1 (2025-05-21)

### Bug Fixes

- **semantic-release**: Adjust remote in pyproject
  ([`301c98a`](https://github.com/russoz-ansible/andebox/commit/301c98aba0c7afc5ac59a66dc3862c9995df8026))

- **semantic-release**: Adjust wf and project defs
  ([`34e53ef`](https://github.com/russoz-ansible/andebox/commit/34e53ef6d0e4a14c2cc013241623a051fd604e30))


## v0.92.0 (2025-05-21)

### Features

- **semantic-release**: Adjust workflow, rename tox action
  ([`3025bdc`](https://github.com/russoz-ansible/andebox/commit/3025bdc43ed993b6b0dba12a5bca77eea4d3e35e))


## v0.91.0 (2025-05-21)

### Chores

- Update poetry.lock
  ([`97c3c77`](https://github.com/russoz-ansible/andebox/commit/97c3c77749d9dce92198c8d333851979ee699f2b))

### Features

- **semantic-release**: Remove all references to bump2version
  ([`4e5cacb`](https://github.com/russoz-ansible/andebox/commit/4e5cacb2a85c9c156a9833d0455f402d5dbc0b99))


## v0.90.0 (2025-05-21)

### Features

- **semantic-release**: Enable automatic semantic release on main
  ([`170e97b`](https://github.com/russoz-ansible/andebox/commit/170e97bcbb51d89c89b54f1fca45d8bfc4274b47))


## v0.89.0 (2025-05-21)

### Features

- **semantic-release**: Using poetry for publishing
  ([`4b8d945`](https://github.com/russoz-ansible/andebox/commit/4b8d94537e59bc559a9ac89b6ee11ca48af9b830))


## v0.88.0 (2025-05-21)

### Features

- **semantic-release**: Add pypi as provider for publishing, again again
  ([`4c2154c`](https://github.com/russoz-ansible/andebox/commit/4c2154c03065647f3ba8689cded53ca8063733f0))


## v0.87.0 (2025-05-21)

### Features

- **semantic-release**: Add pypi as provider for publishing, again
  ([`c3a7d2f`](https://github.com/russoz-ansible/andebox/commit/c3a7d2faf2274aa46a36de4fd99b136d42152713))


## v0.86.0 (2025-05-21)

### Features

- **semantic-release**: Add pypi as provider for publishing
  ([`3a27a72`](https://github.com/russoz-ansible/andebox/commit/3a27a72d02e1b0e35bac2e9dba0c5612f340e10d))


## v0.85.0 (2025-05-21)

### Features

- **semantic-release**: Trigger minor release, and publish
  ([`b3d15fe`](https://github.com/russoz-ansible/andebox/commit/b3d15fef165ba27d3a6082adce28be78ca8ac439))


## v0.84.0 (2025-05-21)

### Features

- **semantic-release**: Trigger minor release, and publish
  ([`28f916b`](https://github.com/russoz-ansible/andebox/commit/28f916bee1ecdad590175c9984c495df105a6eb6))


## v0.83.0 (2025-05-21)

### Chores

- Do not actually release just yet
  ([`a608e06`](https://github.com/russoz-ansible/andebox/commit/a608e068c0a1c59d53c8dd6c4fc1cbb6b83fbb88))

- Do not actually release just yet, but do version
  ([`b4f274d`](https://github.com/russoz-ansible/andebox/commit/b4f274d5c596b62144103acfa011e8e3b013b11c))

- Fix workflow and pyproject.toml
  ([`d9efb0d`](https://github.com/russoz-ansible/andebox/commit/d9efb0dec14a46beaf0b9585634b64cb8ebb2367))

### Features

- **semantic-release**: Trigger minor release
  ([`405f709`](https://github.com/russoz-ansible/andebox/commit/405f709799b49f21ee35192597a44264715454f9))


## v0.82.0 (2025-05-21)

### Chores

- Fix version number
  ([`0665fad`](https://github.com/russoz-ansible/andebox/commit/0665fadf2cb9cdd944250c970aed10d8629f3dfc))

- Remove changelog with wrong version
  ([`edf1344`](https://github.com/russoz-ansible/andebox/commit/edf1344b517b4d77f8086652309469f29a56e32a))

- Version adjustments
  ([`9920a1e`](https://github.com/russoz-ansible/andebox/commit/9920a1e3bfb444b4061b1bd4e8bd78e0958a71eb))

### Features

- Add semantic release ([#59](https://github.com/russoz-ansible/andebox/pull/59),
  [`266ceb8`](https://github.com/russoz-ansible/andebox/commit/266ceb8402df3be74f3f33cbe15b4cb3ec49f211))


## v0.81.0 (2025-05-21)


## v0.80.0 (2025-05-20)


## v0.79.0 (2025-05-18)


## v0.78.0 (2025-05-18)


## v0.77.0 (2025-05-18)


## v0.76.0 (2025-05-17)

### Features

- Make install_requirements command verbose
  ([`5e42fe9`](https://github.com/russoz-ansible/andebox/commit/5e42fe9d926dbfb70c60e3e8562651cc581e2e6d))

- **ansible-test**: -r added to testcase
  ([`c6dae6e`](https://github.com/russoz-ansible/andebox/commit/c6dae6e69eeb69b111c63be2be0fa865d8813490))

- **ansible-test**: -r now accepted for unit test as well
  ([`529e7e9`](https://github.com/russoz-ansible/andebox/commit/529e7e9e629112efe628bb91e1c936c831607b70))


## v0.75.0 (2025-01-26)


## v0.74.0 (2025-01-17)


## v0.73.0 (2025-01-15)


## v0.72.0 (2025-01-11)


## v0.71.0 (2025-01-04)


## v0.70.0 (2025-01-04)


## v0.69.0 (2024-12-31)


## v0.68.0 (2024-12-28)


## v0.67.0 (2024-12-25)


## v0.66.0 (2024-12-23)


## v0.64.0 (2024-12-21)


## v0.63.0 (2024-10-24)


## v0.62.0 (2024-09-17)


## v0.61.0 (2024-09-17)


## v0.60.0 (2024-09-17)


## v0.59.0 (2024-08-04)


## v0.58.0 (2024-08-04)


## v0.57.0 (2024-06-29)


## v0.56.0 (2024-06-28)


## v0.55.0 (2024-06-28)


## v0.52.0 (2024-06-24)


## v0.51.0 (2024-06-15)


## v0.50.0 (2024-06-15)


## v0.49.0 (2023-09-20)


## v0.48.0 (2023-09-20)


## v0.47.0 (2023-06-05)


## v0.46.0 (2023-06-05)


## v0.45.0 (2023-06-05)


## v0.44.0 (2023-06-05)


## v0.43.0 (2023-06-05)


## v0.42.0 (2023-06-05)


## v0.41.0 (2023-06-05)


## v0.40.0 (2023-06-05)


## v0.39.0 (2023-06-05)


## v0.38.0 (2023-06-03)


## v0.37.0 (2023-06-03)


## v0.36.0 (2023-05-20)


## v0.35.0 (2023-04-30)


## v0.34.0 (2023-04-15)


## v0.33.0 (2023-04-08)


## v0.32.0 (2023-04-08)


## v0.31.0 (2023-04-08)


## v0.30.0 (2023-04-08)


## v0.29.0 (2023-04-08)


## v0.28.0 (2023-04-04)


## v0.27.0 (2023-04-02)


## v0.26.0 (2023-01-19)


## v0.24.0 (2022-09-25)


## v0.23.0 (2022-07-22)


## v0.22.0 (2022-04-28)


## v0.21.0 (2022-04-03)


## v0.20.0 (2022-04-03)


## v0.19.0 (2022-04-03)


## v0.18.0 (2022-04-03)


## v0.17.0 (2021-11-27)


## v0.16.0 (2021-11-27)


## v0.15.0 (2021-11-01)


## v0.14.0 (2021-10-09)


## v0.13.1 (2021-07-19)


## v0.13.0 (2021-07-19)


## v0.12.2 (2021-05-19)


## v0.12.1 (2021-05-07)


## v0.12.0 (2021-05-07)


## v0.11.0 (2021-05-06)


## v0.10.0 (2021-04-26)


## v0.9.0 (2021-04-26)


## v0.8.0 (2021-04-26)


## v0.7.0 (2021-04-26)


## v0.6.0 (2021-04-26)


## v0.5.0 (2021-04-11)


## v0.4.0 (2021-04-10)


## v0.3.0 (2021-03-28)


## v0.2.0 (2021-03-25)
