# CHANGELOG


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
