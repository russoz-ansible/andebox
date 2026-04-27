# CHANGELOG


## v2.0.0 (2026-04-27)

### Bug Fixes

- Add support for -- in CLI
  ([`0a3997f`](https://github.com/russoz-ansible/andebox/commit/0a3997f99d808094c5311afc371fab5bc50c2ed9))

With the adoption of typer it was no longer interpreted as a separator of arguments but rather
  passed literally to the underlying command, causing error.

- Configure typer to accept `-h` as an alias for `--help`
  ([`66d928a`](https://github.com/russoz-ansible/andebox/commit/66d928aaa9c4eda62cbde6ad0bb26aa379e1c95e))

- Correct CLI flag name and stale doc examples
  ([`5f804b5`](https://github.com/russoz-ansible/andebox/commit/5f804b5508a7fa9a4ec54a4bedb4ca18bcbe6703))

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Guard against click<8.2.0 missing NoArgsIsHelpError
  ([`121be1a`](https://github.com/russoz-ansible/andebox/commit/121be1a033484bbc7c70097087312f39d11e13df))

NoArgsIsHelpError was introduced in click 8.2.0; CI environments with click 8.1.x raised
  AttributeError when evaluating the except clause. Import it at module load time with a harmless
  fallback for older click.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Chores

- Add CLAUDE.md file
  ([`5818f77`](https://github.com/russoz-ansible/andebox/commit/5818f77861dabeb88f5013efaaf6fb0042d5bae2))

- Adjust wording
  ([`8b04040`](https://github.com/russoz-ansible/andebox/commit/8b040409b475e660c165c24f0474dd440a645eed))

- Adjust year of copyright
  ([`2ff645b`](https://github.com/russoz-ansible/andebox/commit/2ff645b6607d6a7f7289e7fed2ae875121122f03))

- Remove TODO.md, replaced by GitHub issues
  ([`5680f74`](https://github.com/russoz-ansible/andebox/commit/5680f747c0572e9495b5f308a73de65b8244d748))

Items tracked in GH issues #212, #213, #214, #215, #216.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- **deps**: Bump cryptography from 46.0.6 to 46.0.7
  ([`5668528`](https://github.com/russoz-ansible/andebox/commit/56685283e25b7bacdb03bd564d7aced5ab71c5c4))

Bumps [cryptography](https://github.com/pyca/cryptography) from 46.0.6 to 46.0.7. -
  [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pyca/cryptography/compare/46.0.6...46.0.7)

--- updated-dependencies: - dependency-name: cryptography dependency-version: 46.0.7

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group across 1 directory with 2 updates
  ([`77fa9b1`](https://github.com/russoz-ansible/andebox/commit/77fa9b15ee42b4281ab8767b1250f3355f8264cd))

Bumps the python-dependencies group with 1 update in the / directory:
  [typer](https://github.com/fastapi/typer).

Updates `typer` from 0.23.1 to 0.25.0 - [Release notes](https://github.com/fastapi/typer/releases) -
  [Changelog](https://github.com/fastapi/typer/blob/master/docs/release-notes.md) -
  [Commits](https://github.com/fastapi/typer/compare/0.23.1...0.25.0)

Updates `python-semantic-release` from 10.5.3 to 9.21.1 - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v10.5.3...v9.21.1)

--- updated-dependencies: - dependency-name: typer dependency-version: 0.25.0

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies

- dependency-name: python-semantic-release dependency-version: 9.21.1

dependency-type: direct:development

update-type: version-update:semver-major

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 2 updates
  ([`e56c9a0`](https://github.com/russoz-ansible/andebox/commit/e56c9a0944952bde55a9c7d16fe4c8e779386ec3))

Bumps the python-dependencies group with 2 updates: [tox](https://github.com/tox-dev/tox) and
  [pytest](https://github.com/pytest-dev/pytest).

Updates `tox` from 4.52.0 to 4.52.1 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.52.0...4.52.1)

Updates `pytest` from 9.0.2 to 9.0.3 - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/9.0.2...9.0.3)

--- updated-dependencies: - dependency-name: tox dependency-version: 4.52.1

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: pytest dependency-version: 9.0.3

dependency-type: direct:development

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump tox in the python-dependencies group
  ([`cfeb2a8`](https://github.com/russoz-ansible/andebox/commit/cfeb2a8fc71d2e005793d682194869fecec36b4c))

Bumps the python-dependencies group with 1 update: [tox](https://github.com/tox-dev/tox).

Updates `tox` from 4.52.1 to 4.53.0 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.52.1...4.53.0)

--- updated-dependencies: - dependency-name: tox dependency-version: 4.53.0

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump gitpython from 3.1.46 to 3.1.47
  ([`2669745`](https://github.com/russoz-ansible/andebox/commit/26697459ec630865c25d488ba28109af48fa71c1))

Bumps [gitpython](https://github.com/gitpython-developers/GitPython) from 3.1.46 to 3.1.47. -
  [Release notes](https://github.com/gitpython-developers/GitPython/releases) -
  [Changelog](https://github.com/gitpython-developers/GitPython/blob/main/CHANGES) -
  [Commits](https://github.com/gitpython-developers/GitPython/compare/3.1.46...3.1.47)

--- updated-dependencies: - dependency-name: gitpython dependency-version: 3.1.47

dependency-type: direct:development ...

Signed-off-by: dependabot[bot] <support@github.com>

- **devcontainer**: Replace Dockerfile with post-create.sh script
  ([`fe8ba50`](https://github.com/russoz-ansible/andebox/commit/fe8ba50fafcb99ee65a6a4839781d9b8cd48c8c7))

Move pip installs from Dockerfile and postCreateCommand into a single post-create.sh script; switch
  devcontainer.json to use the base image directly. Also replaces tox with poethepoet in the
  bootstrap installs.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- **tooling**: Enforce poetry.lock freshness in CI and pre-commit
  ([`e7e76e3`](https://github.com/russoz-ansible/andebox/commit/e7e76e3beec8181660fea86baa1fe5ebdb562c91))

Add poetry lock --check to all CI workflows and a local pre-commit hook so stale lock files are
  caught before commit and in CI rather than silently regenerated.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- **tooling**: Replace tox/flake8/black/pylint with ruff and poethepoet
  ([`6736c20`](https://github.com/russoz-ansible/andebox/commit/6736c206f3dfcd04d9b735a8ea0a09921c960abf))

- Delete tox.ini, .flake8, .pylintrc - Add ruff.toml with settings ported from .flake8 (line-length,
  E203, complexity, isort) - Add ruff and poethepoet as dev dependencies; remove flake8 and pylint -
  Define poe tasks: test, lint, fmt, check, qa, docs, deps - Replace
  black+flake8+reorder-python-imports pre-commit hooks with ruff-pre-commit - Update CI workflows to
  use ruff check instead of flake8 - Update CLAUDE.md to document new workflow

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- **tooling**: Use poe tasks in GitHub Actions workflows
  ([`c53b484`](https://github.com/russoz-ansible/andebox/commit/c53b484d036c2b9b92e7297879e5ad88ff9a6904))

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Code Style

- Reformat code
  ([`ad82722`](https://github.com/russoz-ansible/andebox/commit/ad8272269f49ebb271efb83aed9305c226ccde07))

- Remove utf-8 coding declarations from all Python files
  ([`db8ba7e`](https://github.com/russoz-ansible/andebox/commit/db8ba7eca3d133b630262203f555bc3f4d65bca2))

Redundant since Python 3 defaults to utf-8.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Continuous Integration

- Remove ai-slop
  ([`6796fdb`](https://github.com/russoz-ansible/andebox/commit/6796fdbd397e97f967492aaf83e9f79eb539b9d4))

### Documentation

- Generate nox-test version matrix table dynamically from VERSION_MATRIX
  ([`922265b`](https://github.com/russoz-ansible/andebox/commit/922265b6bd42bc0f4784a4a413ebda193dcfd4b6))

Adds a list-table (ansible-core × Python) to docs/actions/noxtest.rst, built at Sphinx time from the
  VERSION_MATRIX in noxtest.py so the docs stay in sync automatically. Also expands VERSION_MATRIX
  with the full set of supported Python versions per ansible-core release.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Update asciiciname gifs
  ([`1de70dd`](https://github.com/russoz-ansible/andebox/commit/1de70dded596219d8bc4aaa49cadc563622fb83d))

- Update CLAUDE.md to reflect typer migration
  ([`58e083a`](https://github.com/russoz-ansible/andebox/commit/58e083a1ab5b90a6f08ab5c0833fddfe4932afda))

Replace stale argparse/AndeboxAction plugin system description with the current typer-based
  architecture (modules exposing app = typer.Typer()).

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Update test subcommand examples for typer idiom
  ([`000c192`](https://github.com/russoz-ansible/andebox/commit/000c1920fe69152719a3d25df8c62cd810771c29))

Move the test type argument before '--' to match the typer/Click convention, e.g. `andebox test
  sanity -- --docker ...`.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Features

- Add nox-test action for multi-version ansible testing
  ([`4537f86`](https://github.com/russoz-ansible/andebox/commit/4537f86511fb14d022b6c77fdde2def9d8f171de))

Adds a new `nox-test` action that runs ansible-test within nox across multiple ansible-core and
  Python version combinations. All session definitions are encapsulated inside andebox — no
  noxfile.py required. Sessions are registered programmatically via nox's registry API and executed
  through nox.workflow.execute.

Supports --ansible-core/-a and --python/-p flags to filter the version matrix, plus --session/-s for
  direct session selection. Default run uses one Python per ansible-core version.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- New release
  ([`04eb625`](https://github.com/russoz-ansible/andebox/commit/04eb625cfd4382abc4e5ba3187002ab3d381a7c7))

- Replace argparse/argcomplete with typer
  ([`a18d2f0`](https://github.com/russoz-ansible/andebox/commit/a18d2f0eaebbbe0fdcb4a3870c9f8e5f1d26ee58))

Migrate CLI and all actions from argparse+argcomplete to Typer. Move andebox_context to context.py
  and remove the now-empty actions/base module. Update docs and pyproject.toml accordingly.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Replace argparse/argcomplete with typer
  ([`5b691bf`](https://github.com/russoz-ansible/andebox/commit/5b691bf23fd659fe3df011a4a3261541a05b9e99))

- pyproject.toml: swap argcomplete for typer - context.py: drop argparse Namespace/ArgumentParser;
  add _ErrorReporter that preserves the "andebox: error:" format; create_context(args) now takes a
  SimpleNamespace - actions/base.py: keep AndeboxAction intact; add andebox_context() helper that
  builds the SimpleNamespace from typer ctx.obj + per-action kwargs and chdirs into base_dir -
  cli.py: replace argparse/_make_parser/AndeboxAction discovery with a typer app; discover action
  sub-apps by looking for app: typer.Typer on each action module - actions/*: each module keeps its
  class body unchanged; a thin typer callback and app are appended at the bottom -
  tests/test_andebox_context.py: drop _make_parser dependency; pass SimpleNamespace directly to
  create_context

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>

### Refactoring

- Consolidate features in andebox_context
  ([`41a9248`](https://github.com/russoz-ansible/andebox/commit/41a9248577ad59a3f699b901d76e3dc83d13f6b8))

- temp_tree - collection checks - exception handling

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

- Use pathlib instead of os.*
  ([`9ed0dca`](https://github.com/russoz-ansible/andebox/commit/9ed0dca2e0519b2a00a013728666b8893b9a02ee))

### Testing

- Remove ansible-core 2.17, add 2.21 + devel
  ([`c203687`](https://github.com/russoz-ansible/andebox/commit/c20368759cd5346a04ea2756a212e55205de7978))

Update project dependencies and lock.


## v1.10.0 (2026-04-07)

### Chores

- **deps**: Bump aiohttp from 3.13.2 to 3.13.3
  ([`ac29854`](https://github.com/russoz-ansible/andebox/commit/ac29854d5e5de2520db463ebe144b3de86c05123))

--- updated-dependencies: - dependency-name: aiohttp dependency-version: 3.13.3

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump aiohttp from 3.13.3 to 3.13.4
  ([`d5dbca7`](https://github.com/russoz-ansible/andebox/commit/d5dbca779e674fa24626175bd4083f57c64f8384))

--- updated-dependencies: - dependency-name: aiohttp dependency-version: 3.13.4

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump ansible-core in the python-dependencies group
  ([`ef7fee9`](https://github.com/russoz-ansible/andebox/commit/ef7fee92984cbbe32a679495d070adebddbe9a0a))

Bumps the python-dependencies group with 1 update:
  [ansible-core](https://github.com/ansible/ansible).

Updates `ansible-core` from 2.19.5 to 2.19.6 - [Release
  notes](https://github.com/ansible/ansible/releases) -
  [Commits](https://github.com/ansible/ansible/compare/v2.19.5...v2.19.6)

--- updated-dependencies: - dependency-name: ansible-core dependency-version: 2.19.6

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump antsibull-docs in the python-dependencies group
  ([`8b05ea3`](https://github.com/russoz-ansible/andebox/commit/8b05ea37bd119b686e67081b3edf2ba6edbc6664))

Bumps the python-dependencies group with 1 update:
  [antsibull-docs](https://github.com/ansible-community/antsibull-docs).

Updates `antsibull-docs` from 2.23.0 to 2.24.0 - [Release
  notes](https://github.com/ansible-community/antsibull-docs/releases) -
  [Changelog](https://github.com/ansible-community/antsibull-docs/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/ansible-community/antsibull-docs/compare/2.23.0...2.24.0)

--- updated-dependencies: - dependency-name: antsibull-docs dependency-version: 2.24.0

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump cryptography from 46.0.3 to 46.0.5
  ([`20391d0`](https://github.com/russoz-ansible/andebox/commit/20391d017092ed3c1dd117769fe2fce84f80b177))

Bumps [cryptography](https://github.com/pyca/cryptography) from 46.0.3 to 46.0.5. -
  [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pyca/cryptography/compare/46.0.3...46.0.5)

--- updated-dependencies: - dependency-name: cryptography dependency-version: 46.0.5

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump cryptography from 46.0.5 to 46.0.6
  ([`987379f`](https://github.com/russoz-ansible/andebox/commit/987379f0dbe796ce0ff57a5a803f14d80d7b7ddf))

Bumps [cryptography](https://github.com/pyca/cryptography) from 46.0.5 to 46.0.6. -
  [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pyca/cryptography/compare/46.0.5...46.0.6)

--- updated-dependencies: - dependency-name: cryptography dependency-version: 46.0.6

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump filelock from 3.20.0 to 3.20.1
  ([`4792ba7`](https://github.com/russoz-ansible/andebox/commit/4792ba713951288a8e1cf587e35713d7ee250016))

Bumps [filelock](https://github.com/tox-dev/py-filelock) from 3.20.0 to 3.20.1. - [Release
  notes](https://github.com/tox-dev/py-filelock/releases) -
  [Changelog](https://github.com/tox-dev/filelock/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/py-filelock/compare/3.20.0...3.20.1)

--- updated-dependencies: - dependency-name: filelock dependency-version: 3.20.1

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump filelock from 3.20.2 to 3.20.3
  ([`a45c455`](https://github.com/russoz-ansible/andebox/commit/a45c455ec336d788fffa13385255b75d87dfb74f))

Bumps [filelock](https://github.com/tox-dev/py-filelock) from 3.20.2 to 3.20.3. - [Release
  notes](https://github.com/tox-dev/py-filelock/releases) -
  [Changelog](https://github.com/tox-dev/filelock/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/py-filelock/compare/3.20.2...3.20.3)

--- updated-dependencies: - dependency-name: filelock dependency-version: 3.20.3

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump pygments from 2.19.2 to 2.20.0
  ([`0b43af0`](https://github.com/russoz-ansible/andebox/commit/0b43af003e101a4a526c84061fca45b0b2593afd))

Bumps [pygments](https://github.com/pygments/pygments) from 2.19.2 to 2.20.0. - [Release
  notes](https://github.com/pygments/pygments/releases) -
  [Changelog](https://github.com/pygments/pygments/blob/master/CHANGES) -
  [Commits](https://github.com/pygments/pygments/compare/2.19.2...2.20.0)

--- updated-dependencies: - dependency-name: pygments dependency-version: 2.20.0

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump pynacl from 1.6.1 to 1.6.2
  ([`201aae4`](https://github.com/russoz-ansible/andebox/commit/201aae453ae99901d0174c9a786e0d34ae8bf8c7))

Bumps [pynacl](https://github.com/pyca/pynacl) from 1.6.1 to 1.6.2. -
  [Changelog](https://github.com/pyca/pynacl/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pyca/pynacl/compare/1.6.1...1.6.2)

--- updated-dependencies: - dependency-name: pynacl dependency-version: 1.6.2

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump requests from 2.32.5 to 2.33.0
  ([`ffb6b47`](https://github.com/russoz-ansible/andebox/commit/ffb6b47dabc25f54bea609d6b7c2892dbedbc8c1))

Bumps [requests](https://github.com/psf/requests) from 2.32.5 to 2.33.0. - [Release
  notes](https://github.com/psf/requests/releases) -
  [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md) -
  [Commits](https://github.com/psf/requests/compare/v2.32.5...v2.33.0)

--- updated-dependencies: - dependency-name: requests dependency-version: 2.33.0

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group across 1 directory with 5 updates
  ([`d7c79e5`](https://github.com/russoz-ansible/andebox/commit/d7c79e5d11320bd5dce320fc6c73d84dfefc4652))

Bumps the python-dependencies group with 5 updates in the / directory:

| Package | From | To | | --- | --- | --- | | [ansible-core](https://github.com/ansible/ansible) |
  `2.19.4` | `2.19.5` | | ruamel-yaml | `0.18.16` | `0.18.17` | |
  [pre-commit](https://github.com/pre-commit/pre-commit) | `4.5.0` | `4.5.1` | |
  [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release) |
  `10.5.2` | `10.5.3` | | [furo](https://github.com/pradyunsg/furo) | `2025.9.25` | `2025.12.19` |

Updates `ansible-core` from 2.19.4 to 2.19.5 - [Release
  notes](https://github.com/ansible/ansible/releases) -
  [Commits](https://github.com/ansible/ansible/compare/v2.19.4...v2.19.5)

Updates `ruamel-yaml` from 0.18.16 to 0.18.17

Updates `pre-commit` from 4.5.0 to 4.5.1 - [Release
  notes](https://github.com/pre-commit/pre-commit/releases) -
  [Changelog](https://github.com/pre-commit/pre-commit/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/pre-commit/pre-commit/compare/v4.5.0...v4.5.1)

Updates `python-semantic-release` from 10.5.2 to 10.5.3 - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v10.5.2...v10.5.3)

Updates `furo` from 2025.9.25 to 2025.12.19 - [Release
  notes](https://github.com/pradyunsg/furo/releases) -
  [Changelog](https://github.com/pradyunsg/furo/blob/main/docs/changelog.md) -
  [Commits](https://github.com/pradyunsg/furo/compare/2025.09.25...2025.12.19)

--- updated-dependencies: - dependency-name: ansible-core dependency-version: 2.19.5

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: ruamel-yaml dependency-version: 0.18.17

- dependency-name: pre-commit dependency-version: 4.5.1

dependency-type: direct:development

- dependency-name: python-semantic-release dependency-version: 10.5.3

- dependency-name: furo dependency-version: 2025.12.19

update-type: version-update:semver-minor

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 2 updates
  ([`a23a08a`](https://github.com/russoz-ansible/andebox/commit/a23a08ac7caad3b7a5b0b68807952ff5c546ee76))

Bumps the python-dependencies group with 2 updates: [fabric](https://github.com/fabric/fabric) and
  [tox](https://github.com/tox-dev/tox).

Updates `fabric` from 3.2.2 to 3.2.3 -
  [Commits](https://github.com/fabric/fabric/compare/3.2.2...3.2.3)

Updates `tox` from 4.51.0 to 4.52.0 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.51.0...4.52.0)

--- updated-dependencies: - dependency-name: fabric dependency-version: 3.2.3

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: tox dependency-version: 4.52.0

update-type: version-update:semver-minor

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 2 updates
  ([`39e9fe4`](https://github.com/russoz-ansible/andebox/commit/39e9fe4ab454bc70c677725be9b6cf0ef026ec56))

Bumps the python-dependencies group with 2 updates:
  [ansible-core](https://github.com/ansible/ansible) and [tox](https://github.com/tox-dev/tox).

Updates `ansible-core` from 2.19.7 to 2.19.8 - [Release
  notes](https://github.com/ansible/ansible/releases) -
  [Commits](https://github.com/ansible/ansible/compare/v2.19.7...v2.19.8)

Updates `tox` from 4.50.3 to 4.51.0 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.50.3...4.51.0)

--- updated-dependencies: - dependency-name: ansible-core dependency-version: 2.19.8

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: tox dependency-version: 4.51.0

update-type: version-update:semver-minor

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 2 updates
  ([`469c0e8`](https://github.com/russoz-ansible/andebox/commit/469c0e8012ac3b505bdba9e5061a91ad0e33a9ae))

Bumps the python-dependencies group with 2 updates: [tox](https://github.com/tox-dev/tox) and
  [pytest-cov](https://github.com/pytest-dev/pytest-cov).

Updates `tox` from 4.49.1 to 4.50.3 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.49.1...4.50.3)

Updates `pytest-cov` from 7.0.0 to 7.1.0 -
  [Changelog](https://github.com/pytest-dev/pytest-cov/blob/master/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest-cov/compare/v7.0.0...v7.1.0)

--- updated-dependencies: - dependency-name: tox dependency-version: 4.50.3

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies

- dependency-name: pytest-cov dependency-version: 7.1.0

dependency-type: direct:development

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 2 updates
  ([`2f1ccc6`](https://github.com/russoz-ansible/andebox/commit/2f1ccc6237b5448e52e210dda08831baf9726dd0))

Bumps the python-dependencies group with 2 updates:
  [ansible-core](https://github.com/ansible/ansible) and [tox](https://github.com/tox-dev/tox).

Updates `ansible-core` from 2.19.6 to 2.19.7 - [Release
  notes](https://github.com/ansible/ansible/releases) -
  [Commits](https://github.com/ansible/ansible/compare/v2.19.6...v2.19.7)

Updates `tox` from 4.44.0 to 4.47.0 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.44.0...4.47.0)

--- updated-dependencies: - dependency-name: ansible-core dependency-version: 2.19.7

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: tox dependency-version: 4.47.0

update-type: version-update:semver-minor

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 2 updates
  ([`125cec8`](https://github.com/russoz-ansible/andebox/commit/125cec8a0e2d646bceafc4ab55191e39f8d35485))

Bumps the python-dependencies group with 2 updates: [tox](https://github.com/tox-dev/tox) and
  [pylint](https://github.com/pylint-dev/pylint).

Updates `tox` from 4.36.0 to 4.44.0 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.36.0...4.44.0)

Updates `pylint` from 4.0.4 to 4.0.5 - [Release
  notes](https://github.com/pylint-dev/pylint/releases) -
  [Commits](https://github.com/pylint-dev/pylint/compare/v4.0.4...v4.0.5)

--- updated-dependencies: - dependency-name: tox dependency-version: 4.44.0

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies

- dependency-name: pylint dependency-version: 4.0.5

dependency-type: direct:development

update-type: version-update:semver-patch

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 3 updates
  ([`5811b69`](https://github.com/russoz-ansible/andebox/commit/5811b69c71369b850b0bd8e37f22502213c5b21d))

Bumps the python-dependencies group with 3 updates: [tox](https://github.com/tox-dev/tox),
  ruamel-yaml and [gitpython](https://github.com/gitpython-developers/GitPython).

Updates `tox` from 4.32.0 to 4.33.0 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.32.0...4.33.0)

Updates `ruamel-yaml` from 0.18.17 to 0.19.1

Updates `gitpython` from 3.1.45 to 3.1.46 - [Release
  notes](https://github.com/gitpython-developers/GitPython/releases) -
  [Changelog](https://github.com/gitpython-developers/GitPython/blob/main/CHANGES) -
  [Commits](https://github.com/gitpython-developers/GitPython/compare/3.1.45...3.1.46)

--- updated-dependencies: - dependency-name: tox dependency-version: 4.33.0

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies

- dependency-name: ruamel-yaml dependency-version: 0.19.1

- dependency-name: gitpython dependency-version: 3.1.46

dependency-type: direct:development

update-type: version-update:semver-patch

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump tox in the python-dependencies group
  ([`89faf30`](https://github.com/russoz-ansible/andebox/commit/89faf30a57d0e144335befb2f72b85c313685bd2))

Bumps the python-dependencies group with 1 update: [tox](https://github.com/tox-dev/tox).

Updates `tox` from 4.49.0 to 4.49.1 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.49.0...4.49.1)

--- updated-dependencies: - dependency-name: tox dependency-version: 4.49.1

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump tox in the python-dependencies group
  ([`f18bcc1`](https://github.com/russoz-ansible/andebox/commit/f18bcc13547abb9831b0419f0c85b1c6a7c99cba))

Bumps the python-dependencies group with 1 update: [tox](https://github.com/tox-dev/tox).

Updates `tox` from 4.47.0 to 4.49.0 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.47.0...4.49.0)

--- updated-dependencies: - dependency-name: tox dependency-version: 4.49.0

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump tox in the python-dependencies group
  ([`9bdcc73`](https://github.com/russoz-ansible/andebox/commit/9bdcc73bd4aa9c8c50923b8588f41fc83986de08))

Bumps the python-dependencies group with 1 update: [tox](https://github.com/tox-dev/tox).

Updates `tox` from 4.34.1 to 4.36.0 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.34.1...4.36.0)

--- updated-dependencies: - dependency-name: tox dependency-version: 4.36.0

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump tox in the python-dependencies group
  ([`9aed892`](https://github.com/russoz-ansible/andebox/commit/9aed892faab349421eb90339d8d5b8329de24f94))

Bumps the python-dependencies group with 1 update: [tox](https://github.com/tox-dev/tox).

Updates `tox` from 4.33.0 to 4.34.1 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.33.0...4.34.1)

--- updated-dependencies: - dependency-name: tox dependency-version: 4.34.1

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump urllib3 from 2.6.1 to 2.6.3
  ([`384c7c8`](https://github.com/russoz-ansible/andebox/commit/384c7c82b83b08ef8d87591e61a354e084b599f3))

Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.6.1 to 2.6.3. - [Release
  notes](https://github.com/urllib3/urllib3/releases) -
  [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst) -
  [Commits](https://github.com/urllib3/urllib3/compare/2.6.1...2.6.3)

--- updated-dependencies: - dependency-name: urllib3 dependency-version: 2.6.3

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump virtualenv from 20.35.4 to 20.36.1
  ([`045a31a`](https://github.com/russoz-ansible/andebox/commit/045a31a02043e18890b90146fab2c1875e39e227))

Bumps [virtualenv](https://github.com/pypa/virtualenv) from 20.35.4 to 20.36.1. - [Release
  notes](https://github.com/pypa/virtualenv/releases) -
  [Changelog](https://github.com/pypa/virtualenv/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/pypa/virtualenv/compare/20.35.4...20.36.1)

--- updated-dependencies: - dependency-name: virtualenv dependency-version: 20.36.1

dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump myst-parser from 4.0.1 to 5.0.0
  ([`230a3b7`](https://github.com/russoz-ansible/andebox/commit/230a3b740642ae38c0060b954e0e1c98c0ebea8f))

Bumps [myst-parser](https://github.com/executablebooks/MyST-Parser) from 4.0.1 to 5.0.0. - [Release
  notes](https://github.com/executablebooks/MyST-Parser/releases) -
  [Changelog](https://github.com/executablebooks/MyST-Parser/blob/master/CHANGELOG.md) -
  [Commits](https://github.com/executablebooks/MyST-Parser/compare/v4.0.1...v5.0.0)

--- updated-dependencies: - dependency-name: myst-parser dependency-version: 5.0.0

dependency-type: direct:development

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump sphinx from 8.2.3 to 9.0.4
  ([`b3d5b05`](https://github.com/russoz-ansible/andebox/commit/b3d5b0517ca0ed37792ce51dbd0fd3ef485630b0))

Bumps [sphinx](https://github.com/sphinx-doc/sphinx) from 8.2.3 to 9.0.4. - [Release
  notes](https://github.com/sphinx-doc/sphinx/releases) -
  [Changelog](https://github.com/sphinx-doc/sphinx/blob/v9.0.4/CHANGES.rst) -
  [Commits](https://github.com/sphinx-doc/sphinx/compare/v8.2.3...v9.0.4)

--- updated-dependencies: - dependency-name: sphinx dependency-version: 9.0.4

dependency-type: direct:development

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

### Continuous Integration

- Add `name` to the job
  ([`134f221`](https://github.com/russoz-ansible/andebox/commit/134f221a19cb133837196676c4c054f1bfc52be3))

- Add ansible version as variable in the test matrix
  ([`f7b9204`](https://github.com/russoz-ansible/andebox/commit/f7b9204aab96edcab65e8add31b8c6be4c3ce573))

- Install specific ansible-core within poetry venv
  ([`e5c9d89`](https://github.com/russoz-ansible/andebox/commit/e5c9d89de60c090dfc17ea446331c2c4169d02ee))

- Stop generating coverage for normal (fast) runs
  ([`91871ab`](https://github.com/russoz-ansible/andebox/commit/91871ab5c5e1c38f5abfc51d53cdbba6d88460d0))

- **ansible-core**: Use pip inside poetry
  ([`a4dbd3a`](https://github.com/russoz-ansible/andebox/commit/a4dbd3af027091051160900afc659665d528a9d5))

### Documentation

- **README**: Fix typo in command example
  ([`f4453ef`](https://github.com/russoz-ansible/andebox/commit/f4453ef0520edc2bee1b15534078c6059bc622cb))

It is `andebox test -- units` instead of `unit`

### Features

- **action/tox-test**: Add support to ansible-core 2.21
  ([`0c0f9b4`](https://github.com/russoz-ansible/andebox/commit/0c0f9b480902e6bb26022f11f70ae5983ead3e7a))

### Testing

- **action/test**: Change example in community.general
  ([`2d3707b`](https://github.com/russoz-ansible/andebox/commit/2d3707ba5f95fb7413b5eea93eacc0ebcfe8f5b9))

The ignore entry for `lxc_container` has been removed.


## v1.9.0 (2025-12-08)

### Chores

- **deps**: Bump the python-dependencies group with 4 updates
  ([`97dc508`](https://github.com/russoz-ansible/andebox/commit/97dc5084ef2be7bfc844c93fb2575e1a2ce05795))

Bumps the python-dependencies group with 4 updates:
  [antsibull-docs](https://github.com/ansible-community/antsibull-docs),
  [pylint](https://github.com/pylint-dev/pylint),
  [pre-commit](https://github.com/pre-commit/pre-commit) and
  [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release).

Updates `antsibull-docs` from 2.22.0 to 2.23.0 - [Release
  notes](https://github.com/ansible-community/antsibull-docs/releases) -
  [Changelog](https://github.com/ansible-community/antsibull-docs/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/ansible-community/antsibull-docs/compare/2.22.0...2.23.0)

Updates `pylint` from 4.0.2 to 4.0.3 - [Release
  notes](https://github.com/pylint-dev/pylint/releases) -
  [Commits](https://github.com/pylint-dev/pylint/compare/v4.0.2...v4.0.3)

Updates `pre-commit` from 4.4.0 to 4.5.0 - [Release
  notes](https://github.com/pre-commit/pre-commit/releases) -
  [Changelog](https://github.com/pre-commit/pre-commit/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/pre-commit/pre-commit/compare/v4.4.0...v4.5.0)

Updates `python-semantic-release` from 10.5.1 to 10.5.2 - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v10.5.1...v10.5.2)

--- updated-dependencies: - dependency-name: antsibull-docs dependency-version: 2.23.0

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies

- dependency-name: pylint dependency-version: 4.0.3

dependency-type: direct:development

update-type: version-update:semver-patch

- dependency-name: pre-commit dependency-version: 4.5.0

- dependency-name: python-semantic-release dependency-version: 10.5.2

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Update project dependencies
  ([`716f661`](https://github.com/russoz-ansible/andebox/commit/716f661b6f8dbfbbe3ade37763686793f10d466e))

- **deps-dev**: Bump pytest from 8.4.2 to 9.0.1
  ([`5f427a7`](https://github.com/russoz-ansible/andebox/commit/5f427a7e42c771109509163c50099eba625655cd))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.4.2 to 9.0.1. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.4.2...9.0.1)

--- updated-dependencies: - dependency-name: pytest dependency-version: 9.0.1

dependency-type: direct:development

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

### Features

- Support Python 3.14
  ([`5a8b616`](https://github.com/russoz-ansible/andebox/commit/5a8b61681765b1d5e08d94b5bec59d5cbe1d0d61))


## v1.8.0 (2025-11-17)

### Chores

- Update versions of pre-commit hooks
  ([`2d3a2b0`](https://github.com/russoz-ansible/andebox/commit/2d3a2b07686a54706f3eb2599d9242f6077d4bce))

### Continuous Integration

- Change release workflow from merge to schedule
  ([`2e84a46`](https://github.com/russoz-ansible/andebox/commit/2e84a4602282b1c099d21fc4a4f35b57bc0297a5))

### Documentation

- Capitalise title in usage doc
  ([`f27885c`](https://github.com/russoz-ansible/andebox/commit/f27885caebec9a58c7bed1bc1cae3b9a3772b370))

### Features

- **action/tox-test**: Drop support to ansible-core <2.17, add 2.20
  ([`5c15547`](https://github.com/russoz-ansible/andebox/commit/5c15547b47580de51c61de16100f4ad46662bb12))

- **context**: Add directories to top level exclusion when copying
  ([`53ecc1f`](https://github.com/russoz-ansible/andebox/commit/53ecc1fa35cac1835775ad3baa42652b4478c7da))

- excluding `.nox`, `__pycache__`, `.ansible`, and `.ruff_cache`


## v1.7.1 (2025-11-10)

### Bug Fixes

- Generate andebox --help dynamically for the usage docs
  ([`a34712c`](https://github.com/russoz-ansible/andebox/commit/a34712cbef0382a22f38240eedb8cadd4c6031b0))

### Chores

- Gitignore everything `docs/_build*`
  ([`c4b1f31`](https://github.com/russoz-ansible/andebox/commit/c4b1f313cc4711bd89184f0aa2468c928f9d3ffc))

- **deps**: Bump the python-dependencies group across 1 directory with 4 updates
  ([`2eef30b`](https://github.com/russoz-ansible/andebox/commit/2eef30b8d5c2944d44ba659b5eb64cfa384b8e44))

Bumps the python-dependencies group with 4 updates in the / directory:
  [ansible-core](https://github.com/ansible/ansible),
  [antsibull-docs](https://github.com/ansible-community/antsibull-docs),
  [pre-commit](https://github.com/pre-commit/pre-commit) and
  [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release).

Updates `ansible-core` from 2.19.3 to 2.19.4 - [Release
  notes](https://github.com/ansible/ansible/releases) -
  [Commits](https://github.com/ansible/ansible/compare/v2.19.3...v2.19.4)

Updates `antsibull-docs` from 2.21.0 to 2.22.0 - [Release
  notes](https://github.com/ansible-community/antsibull-docs/releases) -
  [Changelog](https://github.com/ansible-community/antsibull-docs/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/ansible-community/antsibull-docs/compare/2.21.0...2.22.0)

Updates `pre-commit` from 4.3.0 to 4.4.0 - [Release
  notes](https://github.com/pre-commit/pre-commit/releases) -
  [Changelog](https://github.com/pre-commit/pre-commit/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/pre-commit/pre-commit/compare/v4.3.0...v4.4.0)

Updates `python-semantic-release` from 10.4.1 to 10.5.1 - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v10.4.1...v10.5.1)

--- updated-dependencies: - dependency-name: ansible-core dependency-version: 2.19.4

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: antsibull-docs dependency-version: 2.22.0

update-type: version-update:semver-minor

- dependency-name: pre-commit dependency-version: 4.4.0

dependency-type: direct:development

- dependency-name: python-semantic-release dependency-version: 10.5.1

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 2 updates
  ([`4287c50`](https://github.com/russoz-ansible/andebox/commit/4287c50ae5ade9d6d6673b0e47d68e463ff43261))

Bumps the python-dependencies group with 2 updates:
  [argcomplete](https://github.com/kislyuk/argcomplete) and
  [pylint](https://github.com/pylint-dev/pylint).

Updates `argcomplete` from 3.6.2 to 3.6.3 - [Release
  notes](https://github.com/kislyuk/argcomplete/releases) -
  [Changelog](https://github.com/kislyuk/argcomplete/blob/main/Changes.rst) -
  [Commits](https://github.com/kislyuk/argcomplete/compare/v3.6.2...v3.6.3)

Updates `pylint` from 4.0.0 to 4.0.1 - [Release
  notes](https://github.com/pylint-dev/pylint/releases) -
  [Commits](https://github.com/pylint-dev/pylint/compare/v4.0.0...v4.0.1)

--- updated-dependencies: - dependency-name: argcomplete dependency-version: 3.6.3

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: pylint dependency-version: 4.0.1

dependency-type: direct:development

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 2 updates
  ([`9a53188`](https://github.com/russoz-ansible/andebox/commit/9a5318880e4ed0de57e9834759f78d9c8ca46ac8))

Bumps the python-dependencies group with 2 updates:
  [ansible-core](https://github.com/ansible/ansible) and [tox](https://github.com/tox-dev/tox).

Updates `ansible-core` from 2.19.2 to 2.19.3 - [Release
  notes](https://github.com/ansible/ansible/releases) -
  [Commits](https://github.com/ansible/ansible/compare/v2.19.2...v2.19.3)

Updates `tox` from 4.30.3 to 4.31.0 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.30.3...4.31.0)

--- updated-dependencies: - dependency-name: ansible-core dependency-version: 2.19.3

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: tox dependency-version: 4.31.0

update-type: version-update:semver-minor

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 3 updates
  ([`b4eff45`](https://github.com/russoz-ansible/andebox/commit/b4eff4504c5b94a7b8f6cd160e7834033627caf9))

Bumps the python-dependencies group with 3 updates: [tox](https://github.com/tox-dev/tox),
  ruamel-yaml and [pylint](https://github.com/pylint-dev/pylint).

Updates `tox` from 4.31.0 to 4.32.0 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.31.0...4.32.0)

Updates `ruamel-yaml` from 0.18.15 to 0.18.16

Updates `pylint` from 4.0.1 to 4.0.2 - [Release
  notes](https://github.com/pylint-dev/pylint/releases) -
  [Commits](https://github.com/pylint-dev/pylint/compare/v4.0.1...v4.0.2)

--- updated-dependencies: - dependency-name: tox dependency-version: 4.32.0

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies

- dependency-name: ruamel-yaml dependency-version: 0.18.16

update-type: version-update:semver-patch

- dependency-name: pylint dependency-version: 4.0.2

dependency-type: direct:development

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump pylint from 3.3.9 to 4.0.0
  ([`af5882b`](https://github.com/russoz-ansible/andebox/commit/af5882b2b3ae9b63b032c8381223f357ecdb4212))

Bumps [pylint](https://github.com/pylint-dev/pylint) from 3.3.9 to 4.0.0. - [Release
  notes](https://github.com/pylint-dev/pylint/releases) -
  [Commits](https://github.com/pylint-dev/pylint/compare/v3.3.9...v4.0.0)

--- updated-dependencies: - dependency-name: pylint dependency-version: 4.0.0

dependency-type: direct:development

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

- **devcontainer**: Pin base image to Python 3.13, Debian bookworm
  ([`96eba87`](https://github.com/russoz-ansible/andebox/commit/96eba8732247fbe98cf2a58f6a5c549a9ea36d8a))

### Refactoring

- Use contextlib.chdir() instead of custom context manager
  ([`d99f6c2`](https://github.com/russoz-ansible/andebox/commit/d99f6c2623e28f7078df169956080417d667eb47))


## v1.7.0 (2025-10-11)

### Chores

- **action/vagrant**: Adjust usage and epilog for CLI help
  ([`d6a8dda`](https://github.com/russoz-ansible/andebox/commit/d6a8dda60324e142acb5a532cd0f1d8218fb805c))

- **action/vagrant**: Adjust usage and epilog for CLI help
  ([`8c5dd35`](https://github.com/russoz-ansible/andebox/commit/8c5dd352bb5a0dcc63c84e28db06f4d51687a4e1))

- **deps**: Bump the python-dependencies group across 1 directory with 3 updates
  ([`4dfce4b`](https://github.com/russoz-ansible/andebox/commit/4dfce4b3f49d7d5064ea1cc3c406988427204c5f))

Bumps the python-dependencies group with 3 updates in the / directory:
  [ansible-core](https://github.com/ansible/ansible),
  [pytest-mock](https://github.com/pytest-dev/pytest-mock) and
  [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release).

Updates `ansible-core` from 2.19.1 to 2.19.2 - [Release
  notes](https://github.com/ansible/ansible/releases) -
  [Commits](https://github.com/ansible/ansible/compare/v2.19.1...v2.19.2)

Updates `pytest-mock` from 3.15.0 to 3.15.1 - [Release
  notes](https://github.com/pytest-dev/pytest-mock/releases) -
  [Changelog](https://github.com/pytest-dev/pytest-mock/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest-mock/compare/v3.15.0...v3.15.1)

Updates `python-semantic-release` from 10.4.0 to 10.4.1 - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v10.4...v10.4.1)

--- updated-dependencies: - dependency-name: ansible-core dependency-version: 2.19.2

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: pytest-mock dependency-version: 3.15.1

dependency-type: direct:development

- dependency-name: python-semantic-release dependency-version: 10.4.1

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 2 updates
  ([`82fee57`](https://github.com/russoz-ansible/andebox/commit/82fee578dddd3ea33f09e0255adac14be8219c91))

Bumps the python-dependencies group with 2 updates: [tox](https://github.com/tox-dev/tox) and
  [pylint](https://github.com/pylint-dev/pylint).

Updates `tox` from 4.30.2 to 4.30.3 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.30.2...4.30.3)

Updates `pylint` from 3.3.8 to 3.3.9 - [Release
  notes](https://github.com/pylint-dev/pylint/releases) -
  [Commits](https://github.com/pylint-dev/pylint/compare/v3.3.8...v3.3.9)

--- updated-dependencies: - dependency-name: tox dependency-version: 4.30.3

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: pylint dependency-version: 3.3.9

dependency-type: direct:development

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 2 updates
  ([`8f152ce`](https://github.com/russoz-ansible/andebox/commit/8f152cea38ca7bbef3393d05002e33d27e38e08d))

Bumps the python-dependencies group with 2 updates: [pyyaml](https://github.com/yaml/pyyaml) and
  [furo](https://github.com/pradyunsg/furo).

Updates `pyyaml` from 6.0.2 to 6.0.3 - [Release notes](https://github.com/yaml/pyyaml/releases) -
  [Changelog](https://github.com/yaml/pyyaml/blob/6.0.3/CHANGES) -
  [Commits](https://github.com/yaml/pyyaml/compare/6.0.2...6.0.3)

Updates `furo` from 2025.7.19 to 2025.9.25 - [Release
  notes](https://github.com/pradyunsg/furo/releases) -
  [Changelog](https://github.com/pradyunsg/furo/blob/main/docs/changelog.md) -
  [Commits](https://github.com/pradyunsg/furo/compare/2025.07.19...2025.09.25)

--- updated-dependencies: - dependency-name: pyyaml dependency-version: 6.0.3

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: furo dependency-version: 2025.9.25

dependency-type: direct:development

update-type: version-update:semver-minor

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 2 updates
  ([`710b775`](https://github.com/russoz-ansible/andebox/commit/710b7759120a8634ba1523df3f480297798acfe3))

Bumps the python-dependencies group with 2 updates:
  [ansible-core](https://github.com/ansible/ansible) and [tox](https://github.com/tox-dev/tox).

Updates `ansible-core` from 2.19.0 to 2.19.1 - [Release
  notes](https://github.com/ansible/ansible/releases) -
  [Commits](https://github.com/ansible/ansible/compare/v2.19.0...v2.19.1)

Updates `tox` from 4.28.4 to 4.29.0 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.28.4...4.29.0)

--- updated-dependencies: - dependency-name: ansible-core dependency-version: 2.19.1

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: tox dependency-version: 4.29.0

update-type: version-update:semver-minor

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 5 updates
  ([`9655c79`](https://github.com/russoz-ansible/andebox/commit/9655c79a3bec0d261de28619bc3cf13804c63c2c))

Bumps the python-dependencies group with 5 updates:

| Package | From | To | | --- | --- | --- | | [tox](https://github.com/tox-dev/tox) | `4.29.0` |
  `4.30.2` | | [pytest](https://github.com/pytest-dev/pytest) | `8.4.1` | `8.4.2` | |
  [pytest-mock](https://github.com/pytest-dev/pytest-mock) | `3.14.1` | `3.15.0` | |
  [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release) |
  `10.3.1` | `10.4.0` | | [pytest-cov](https://github.com/pytest-dev/pytest-cov) | `6.2.1` | `6.3.0`
  |

Updates `tox` from 4.29.0 to 4.30.2 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.29.0...4.30.2)

Updates `pytest` from 8.4.1 to 8.4.2 - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.4.1...8.4.2)

Updates `pytest-mock` from 3.14.1 to 3.15.0 - [Release
  notes](https://github.com/pytest-dev/pytest-mock/releases) -
  [Changelog](https://github.com/pytest-dev/pytest-mock/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest-mock/compare/v3.14.1...v3.15.0)

Updates `python-semantic-release` from 10.3.1 to 10.4.0 - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v10.3.1...v10.4)

Updates `pytest-cov` from 6.2.1 to 6.3.0 -
  [Changelog](https://github.com/pytest-dev/pytest-cov/blob/master/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest-cov/compare/v6.2.1...v6.3.0)

--- updated-dependencies: - dependency-name: tox dependency-version: 4.30.2

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies

- dependency-name: pytest dependency-version: 8.4.2

dependency-type: direct:development

update-type: version-update:semver-patch

- dependency-name: pytest-mock dependency-version: 3.15.0

- dependency-name: python-semantic-release dependency-version: 10.4.0

- dependency-name: pytest-cov dependency-version: 6.3.0

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump pytest-cov from 6.3.0 to 7.0.0
  ([`378c4b1`](https://github.com/russoz-ansible/andebox/commit/378c4b1edcbf3a1efa0a05a1bb55e29263c5c7cb))

Bumps [pytest-cov](https://github.com/pytest-dev/pytest-cov) from 6.3.0 to 7.0.0. -
  [Changelog](https://github.com/pytest-dev/pytest-cov/blob/master/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest-cov/compare/v6.3.0...v7.0.0)

--- updated-dependencies: - dependency-name: pytest-cov dependency-version: 7.0.0

dependency-type: direct:development

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

### Documentation

- Improve example and fix typo
  ([`f52d724`](https://github.com/russoz-ansible/andebox/commit/f52d72443dee05071848ed57730f5da00ecb885a))

- **action/vagrant**: Fix typo
  ([`aa515bb`](https://github.com/russoz-ansible/andebox/commit/aa515bb9e0623cf60b4a8a63825b1a509bd53055))

- **action/vagrant**: Improve clarity of text
  ([`507c66e`](https://github.com/russoz-ansible/andebox/commit/507c66e756fa43fb20b042ffe056f89bc4f3e70b))

- **actions**: Remove redundant block
  ([`ef1fe7f`](https://github.com/russoz-ansible/andebox/commit/ef1fe7fb6e98143932786899332ca6ceddc4d84c))

### Features

- Make CLI parser available to context
  ([`0c5eb83`](https://github.com/russoz-ansible/andebox/commit/0c5eb83f0b75bfde2a8f1e349886aa713e39dacb))

- **action/test**: Improve help message for validated args
  ([`ca78820`](https://github.com/russoz-ansible/andebox/commit/ca78820fe9b45428a967ed6e29e6af0bdde2fe82))

- **action/test**: Validate some args combination
  ([`7b94f65`](https://github.com/russoz-ansible/andebox/commit/7b94f651f7f80b4342b4d6137ee5caacede6c9b0))

- -R cannot be used with sanity - -ei can only be used with sanity

- **cli**: Chance exit code for keyboard interrupt to 100
  ([`a0a1b91`](https://github.com/russoz-ansible/andebox/commit/a0a1b91ec6a8d0013559874e8816bce92b61bf47))

To prevent clashing with ArgParser parameter validation which returns 2.

### Testing

- Capture SystemExit in cli.run() to be able to test it
  ([`ce14782`](https://github.com/russoz-ansible/andebox/commit/ce147824bc58ada79775817436495f3775c12540))

- Match any line number in cg-sanity-exclude-ignore
  ([`a0c06bf`](https://github.com/russoz-ansible/andebox/commit/a0c06bf0b929fc0de4e11391685ce77923c909c2))

- **action/test**: Test using `--exclude-from-ignore`
  ([`0f7bf5f`](https://github.com/russoz-ansible/andebox/commit/0f7bf5f13285bc960596bc68291dd0d4dfe97717))


## v1.6.0 (2025-08-30)

### Chores

- Run tests when updating dependencies
  ([`2b883a2`](https://github.com/russoz-ansible/andebox/commit/2b883a2157a65131e987c7044421306a98c12a00))

- **deps**: Bump the python-dependencies group across 1 directory with 4 updates
  ([`42d377b`](https://github.com/russoz-ansible/andebox/commit/42d377b96e9075bbd87b56a062b6a6f02ff55ac1))

Bumps the python-dependencies group with 4 updates in the / directory: ruamel-yaml,
  [antsibull-docs](https://github.com/ansible-community/antsibull-docs),
  [pylint](https://github.com/pylint-dev/pylint) and
  [pre-commit](https://github.com/pre-commit/pre-commit).

Updates `ruamel-yaml` from 0.18.12 to 0.18.15

Updates `antsibull-docs` from 2.20.0 to 2.21.0 - [Release
  notes](https://github.com/ansible-community/antsibull-docs/releases) -
  [Changelog](https://github.com/ansible-community/antsibull-docs/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/ansible-community/antsibull-docs/compare/2.20.0...2.21.0)

Updates `pylint` from 3.3.7 to 3.3.8 - [Release
  notes](https://github.com/pylint-dev/pylint/releases) -
  [Commits](https://github.com/pylint-dev/pylint/compare/v3.3.7...v3.3.8)

Updates `pre-commit` from 4.2.0 to 4.3.0 - [Release
  notes](https://github.com/pre-commit/pre-commit/releases) -
  [Changelog](https://github.com/pre-commit/pre-commit/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/pre-commit/pre-commit/compare/v4.2.0...v4.3.0)

--- updated-dependencies: - dependency-name: ruamel-yaml dependency-version: 0.18.15

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: antsibull-docs dependency-version: 2.21.0

update-type: version-update:semver-minor

- dependency-name: pylint dependency-version: 3.3.8

dependency-type: direct:development

- dependency-name: pre-commit dependency-version: 4.3.0

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the python-dependencies group with 3 updates
  ([`f5f077b`](https://github.com/russoz-ansible/andebox/commit/f5f077be8476c2c7fd16e1afa0e84e3e945cb24d))

Bumps the python-dependencies group with 3 updates:
  [ansible-core](https://github.com/ansible/ansible), [tox](https://github.com/tox-dev/tox) and
  [antsibull-docs](https://github.com/ansible-community/antsibull-docs).

Updates `ansible-core` from 2.18.6 to 2.18.7 - [Release
  notes](https://github.com/ansible/ansible/releases) -
  [Commits](https://github.com/ansible/ansible/compare/v2.18.6...v2.18.7)

Updates `tox` from 4.27.0 to 4.28.0 - [Release notes](https://github.com/tox-dev/tox/releases) -
  [Changelog](https://github.com/tox-dev/tox/blob/main/docs/changelog.rst) -
  [Commits](https://github.com/tox-dev/tox/compare/4.27.0...4.28.0)

Updates `antsibull-docs` from 2.18.0 to 2.19.1 - [Release
  notes](https://github.com/ansible-community/antsibull-docs/releases) -
  [Changelog](https://github.com/ansible-community/antsibull-docs/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/ansible-community/antsibull-docs/compare/2.18.0...2.19.1)

--- updated-dependencies: - dependency-name: ansible-core dependency-version: 2.18.7

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: python-dependencies

- dependency-name: tox dependency-version: 4.28.0

update-type: version-update:semver-minor

- dependency-name: antsibull-docs dependency-version: 2.19.1

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Update project dependencies
  ([`ed2d793`](https://github.com/russoz-ansible/andebox/commit/ed2d79340a9796707dbe0894472ae110a6098223))

- **deps-dev**: Bump furo from 2024.8.6 to 2025.7.19
  ([`c779ee6`](https://github.com/russoz-ansible/andebox/commit/c779ee6042cbea608151e67dcb56ebacc70293eb))

Bumps [furo](https://github.com/pradyunsg/furo) from 2024.8.6 to 2025.7.19. - [Release
  notes](https://github.com/pradyunsg/furo/releases) -
  [Changelog](https://github.com/pradyunsg/furo/blob/main/docs/changelog.md) -
  [Commits](https://github.com/pradyunsg/furo/compare/2024.08.06...2025.07.19)

--- updated-dependencies: - dependency-name: furo dependency-version: 2025.7.19

dependency-type: direct:development

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

### Features

- **action/tox-test**: Update default tox ini up to ansible-core 2.19
  ([`fbb8ef2`](https://github.com/russoz-ansible/andebox/commit/fbb8ef2b07d07f898c5125f300382522b22d90b0))

### Testing

- Adjust output for test of action/yaml-doc
  ([`1e3f637`](https://github.com/russoz-ansible/andebox/commit/1e3f63787331056ba89bb468e2bc6f00fa53f314))

- **action/test**: Skip Python 3.11 when using ansible-core's ansible-test
  ([`a042008`](https://github.com/russoz-ansible/andebox/commit/a0420082bf6296eea7453bec8968e8a325c4ef99))


## v1.5.1 (2025-07-23)

### Bug Fixes

- **action/yaml-doc**: Fix the rewrapping of long lines
  ([`82cfc60`](https://github.com/russoz-ansible/andebox/commit/82cfc60069d24c32b1f3a00124e1c02de759e0a3))

When a long line is already split in two, ruamel.yaml seems to be adding a trailing space to the
  first line.


## v1.5.0 (2025-07-13)

### Chores

- Adjust tox deps action to conventional commits
  ([`23dec08`](https://github.com/russoz-ansible/andebox/commit/23dec08e79da847079a9cdd48ae49d74f82a2803))

- **deps**: Bump the python-dependencies group with 2 updates
  ([`8f77cb6`](https://github.com/russoz-ansible/andebox/commit/8f77cb64b44c8420d628258786f0b691ac9b6359))

Bumps the python-dependencies group with 2 updates:
  [antsibull-docs](https://github.com/ansible-community/antsibull-docs) and
  [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release).

Updates `antsibull-docs` from 2.17.1 to 2.18.0 - [Release
  notes](https://github.com/ansible-community/antsibull-docs/releases) -
  [Changelog](https://github.com/ansible-community/antsibull-docs/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/ansible-community/antsibull-docs/compare/2.17.1...2.18.0)

Updates `python-semantic-release` from 10.1.0 to 10.2.0 - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v10.1...v10.2)

--- updated-dependencies: - dependency-name: antsibull-docs dependency-version: 2.18.0

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies

- dependency-name: python-semantic-release dependency-version: 10.2.0

dependency-type: direct:development

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump urllib3 from 2.4.0 to 2.5.0 in the pip group
  ([`79f096f`](https://github.com/russoz-ansible/andebox/commit/79f096fcaf42036f9cfc820be5093ad49e0129dc))

Bumps the pip group with 1 update: [urllib3](https://github.com/urllib3/urllib3).

Updates `urllib3` from 2.4.0 to 2.5.0 - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst) -
  [Commits](https://github.com/urllib3/urllib3/compare/2.4.0...2.5.0)

--- updated-dependencies: - dependency-name: urllib3 dependency-version: 2.5.0

dependency-type: indirect

dependency-group: pip ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Update project dependencies
  ([`4c543ce`](https://github.com/russoz-ansible/andebox/commit/4c543ceeb0ad5bd3c97604888c51c0d04e1ccaf6))

- **devcontainer**: Comment out settings for ssh-agent
  ([`7181cf1`](https://github.com/russoz-ansible/andebox/commit/7181cf137695fec484ba1098b80c55f4d805a31f))

### Documentation

- **TODO**: Remove TODO entry for documenting actions
  ([`3dd5bcc`](https://github.com/russoz-ansible/andebox/commit/3dd5bcc92fa1038d6793aa98b36bad436ac2e606))

### Features

- **action/vagrant**: Suppress warning message for missing vagrant binary
  ([`72fbe46`](https://github.com/russoz-ansible/andebox/commit/72fbe46dc1fb250cec1c5bb26ca9e08318886e9d))

- **action/yaml-doc**: Improve error handling for JSON parsing of samples
  ([`5f92c7b`](https://github.com/russoz-ansible/andebox/commit/5f92c7bbbb6a940e42f812ca345a12bfd42f9f8d))

### Testing

- List all ignore lines in basic test
  ([`a48ee29`](https://github.com/russoz-ansible/andebox/commit/a48ee29a4954d25ef07875283962b7899570bce8))


## v1.4.3 (2025-06-18)

### Bug Fixes

- Force patch release
  ([`743814b`](https://github.com/russoz-ansible/andebox/commit/743814baa91da6e283b5396a0092e1ac66e70666))

### Chores

- **deps-dev**: Bump the python-dependencies group with 2 updates
  ([`c410c87`](https://github.com/russoz-ansible/andebox/commit/c410c875425db7c2ecc06ea7e050d6e99d9fab04))

Bumps the python-dependencies group with 2 updates:
  [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release) and
  [pytest-cov](https://github.com/pytest-dev/pytest-cov).

Updates `python-semantic-release` from 10.0.2 to 10.1.0 - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v10.0.2...v10.1)

Updates `pytest-cov` from 6.1.1 to 6.2.1 -
  [Changelog](https://github.com/pytest-dev/pytest-cov/blob/master/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest-cov/compare/v6.1.1...v6.2.1)

--- updated-dependencies: - dependency-name: python-semantic-release dependency-version: 10.1.0

dependency-type: direct:development

update-type: version-update:semver-minor

dependency-group: python-dependencies

- dependency-name: pytest-cov dependency-version: 6.2.1

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

### Documentation

- Revamp the high-level doc page for actions
  ([`9860942`](https://github.com/russoz-ansible/andebox/commit/986094258ba81abf56b270f99fd6e648509a0fa3))

### Testing

- Fix some edge cases when `sample` is JSON content
  ([`a271a74`](https://github.com/russoz-ansible/andebox/commit/a271a74223b3ffdc3008209eba64850b1295f77a))


## v1.4.2 (2025-06-15)

### Bug Fixes

- Ignore EXAMPLES with multiple YAML docs
  ([`8c3b05b`](https://github.com/russoz-ansible/andebox/commit/8c3b05bcb076ff1a8328527520ba37c5fe5a03a0))


## v1.4.1 (2025-06-14)

### Bug Fixes

- Fix action docsite test
  ([`1a9a278`](https://github.com/russoz-ansible/andebox/commit/1a9a278743808c54ef98bdd67293f7d93e4d756b))

Submitting this as a fix to ensure the new release process is triggered.


## v1.4.0 (2025-06-14)

### Chores

- Use safer release process
  ([`cfa9911`](https://github.com/russoz-ansible/andebox/commit/cfa9911e6b628523ba295617bbadfbbda2ce3ebf))

### Features

- Use asciinwriter to generate term demos
  ([`5951dfd`](https://github.com/russoz-ansible/andebox/commit/5951dfd73be8d2e8e680f47828664c8796ff37ae))


## v1.3.1 (2025-06-11)

### Bug Fixes

- **deps**: Update dependencies
  ([`642334c`](https://github.com/russoz-ansible/andebox/commit/642334c29710c6b819933a4b6a85d5922336a7ad))

### Chores

- **ai-prompt**: Rename prompt file
  ([`96f1487`](https://github.com/russoz-ansible/andebox/commit/96f1487e3321d69889d059c5af50c0897ddd149e))

### Refactoring

- Make attributes input and expected immutables in GenericTestCase
  ([`3f84646`](https://github.com/russoz-ansible/andebox/commit/3f846466e9412622f2bb05a575dccd8681df8604))

- Move attribute data from the helper to GenericTestCase
  ([`a296cda`](https://github.com/russoz-ansible/andebox/commit/a296cdaab77cf93f8a6f75f4d5425028b55fea20))

- Standardize test helpers to use GenericTestCase, rename execute to run
  ([`4a6b748`](https://github.com/russoz-ansible/andebox/commit/4a6b7482a391a548ba0ceaba29af4e8337da149a))

### Testing

- Add debugging info, rename test functions
  ([`7de1c23`](https://github.com/russoz-ansible/andebox/commit/7de1c23c69ed1953f248a4d6300ec0965289c970))


## v1.3.0 (2025-06-09)

### Bug Fixes

- Make sphinx a dependency for andebox, as required by docsite action
  ([`d4be373`](https://github.com/russoz-ansible/andebox/commit/d4be3736efcc544c79089082110c025ca6d5e312))

### Chores

- Add CHANGELOG URL to the project
  ([`5e7949b`](https://github.com/russoz-ansible/andebox/commit/5e7949bc669e43183ee4c42d2b8277a987675bb0))

### Documentation

- Add documentation for actions
  ([`6450e53`](https://github.com/russoz-ansible/andebox/commit/6450e53466b501fcdf00f5018ff5b129c99e85be))

### Features

- **action/docsite**: Make destination arg required
  ([`6a325da`](https://github.com/russoz-ansible/andebox/commit/6a325da886eb9b5752f8ea4c1e8a9b9c6ac2cd23))


## v1.2.3 (2025-06-09)

### Bug Fixes

- Adjust error message for unknown context
  ([`735e621`](https://github.com/russoz-ansible/andebox/commit/735e6216b9f526aeae5a7e9874bb066f3aa7ebd2))


## v1.2.2 (2025-06-09)

### Bug Fixes

- Remove extraneous dependencies
  ([`beec4a3`](https://github.com/russoz-ansible/andebox/commit/beec4a355c7ed27566daefd10c15b32e7263b9aa))

### Chores

- Remove commitizen and references to ti
  ([`a69b6c9`](https://github.com/russoz-ansible/andebox/commit/a69b6c9eafbade075825ec19772e168759d6c410))

- Update poetry.lock
  ([`f2dfd0a`](https://github.com/russoz-ansible/andebox/commit/f2dfd0a881a0a1011334c0d05bbcbb46f3307d96))

### Continuous Integration

- Undo commit: update workflows to lock deps sooner rather than later
  ([`fceafa3`](https://github.com/russoz-ansible/andebox/commit/fceafa325ecaf0e3b3067748596e0bf04893afc4))

- Update workflows to lock deps sooner rather than later
  ([`6404eb6`](https://github.com/russoz-ansible/andebox/commit/6404eb60ac3b3513695a71b7bf50f7464ef20cc2))


## v1.2.1 (2025-06-06)

### Bug Fixes

- **semantic-release**: Trying to fix the CHANGELOG generation
  ([`95a6419`](https://github.com/russoz-ansible/andebox/commit/95a6419fb2f89ee7852f83b634f0d6b3e222c565))


## v1.2.0 (2025-06-05)

### Chores

- **deps**: Bump the python-dependencies group across 1 directory with 2 updates
  ([`0a428ef`](https://github.com/russoz-ansible/andebox/commit/0a428ef08ca8be4465d93334269d64ab0e078822))

Bumps the python-dependencies group with 2 updates in the / directory:
  [antsibull-docs](https://github.com/ansible-community/antsibull-docs) and
  [pytest](https://github.com/pytest-dev/pytest).

Updates `antsibull-docs` from 2.16.3 to 2.17.0 - [Release
  notes](https://github.com/ansible-community/antsibull-docs/releases) -
  [Changelog](https://github.com/ansible-community/antsibull-docs/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/ansible-community/antsibull-docs/compare/2.16.3...2.17.0)

Updates `pytest` from 8.3.5 to 8.4.0 - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.3.5...8.4.0)

--- updated-dependencies: - dependency-name: antsibull-docs dependency-version: 2.17.0

dependency-type: direct:production

update-type: version-update:semver-minor

dependency-group: python-dependencies

- dependency-name: pytest dependency-version: 8.4.0

dependency-type: direct:development

dependency-group: python-dependencies ...

Signed-off-by: dependabot[bot] <support@github.com>

- **tox**: Update tox action `docs` to install the namesake group in the poetry venv
  ([`f0405f4`](https://github.com/russoz-ansible/andebox/commit/f0405f42817493789579a6c340551d17ed54a553))

### Continuous Integration

- Fix typo in workflow
  ([`7f70245`](https://github.com/russoz-ansible/andebox/commit/7f70245bbc9500886214259b2773d8346fc8afb5))

### Documentation

- **ascii-demo**: Add pexpect to pyproject docs group
  ([`b908843`](https://github.com/russoz-ansible/andebox/commit/b908843e8cef200a8f672a7465593a84ab8deda8))

- **ascii-demo**: Add README file for docs/images/term
  ([`55bff66`](https://github.com/russoz-ansible/andebox/commit/55bff669bc96189fe80b4da59d2012da6b7bea8e))

### Features

- **action/ignores**: Remove restriction to spec parameter
  ([`d4dea99`](https://github.com/russoz-ansible/andebox/commit/d4dea99a4634b9e04d73070a0e741be7629afdc9))

Parameter was previously restricted t a list of choices based on the existing filenames. Now not
  only that restriction is completely gone, but the parameter itself has been renamed from
  `--ignore-file-spec` (or `-ifs`) to `--spec` (or `-s`). Tests have been updated and the two xfail
  tests are now passing. Dependency `looseversion` is no lonoger used and has been removed from the
  project.

### Refactoring

- Move definition of `__version__` to `andebox/__init.py__`
  ([`d40caa9`](https://github.com/russoz-ansible/andebox/commit/d40caa92f4fbb5ae7f3b7f519615b459f22f507c))

### Testing

- **coverage**: Do not generate coverage by default
  ([`ba1c31b`](https://github.com/russoz-ansible/andebox/commit/ba1c31b661d0b16bd0c4382a9c7c87a5778f25b2))

That should streamline local builds, but the CI workflows now run `pytest --cov` to force the
  generation of coverage information.


## v1.1.2 (2025-06-03)

### Bug Fixes

- **action/yaml-doc**: Fix the wrapping of long lines
  ([`8bb120c`](https://github.com/russoz-ansible/andebox/commit/8bb120c01d9ca0f06cc0c5a56a42f78e7b6216d3))

### Chores

- **ai-prompt**: Refine the Python developer aspect
  ([`993ad3b`](https://github.com/russoz-ansible/andebox/commit/993ad3b12462144d518e665d2e1bcc21852f0abf))

- **license**: Make project SPDX compliant
  ([`b9cdd66`](https://github.com/russoz-ansible/andebox/commit/b9cdd66aeca1f691d07389903cf1b60a935275fc))

- **license**: Make project SPDX compliant
  ([`213fad6`](https://github.com/russoz-ansible/andebox/commit/213fad6fae7b5c38255954427d799cc18ef8e7be))

### Continuous Integration

- **slow-test**: Add weekly workflow for slow tests
  ([`68e1a9e`](https://github.com/russoz-ansible/andebox/commit/68e1a9e0b9b09e9cc6cebea51f384c6b0fbd6ba4))

### Testing

- Remove flags to skip python 3.9 and 3.10
  ([`18f7842`](https://github.com/russoz-ansible/andebox/commit/18f7842c9d1d0098bfe4524b70f5b851ce287d48))

- **action/docsite**: Add marker for slow test
  ([`5ef4552`](https://github.com/russoz-ansible/andebox/commit/5ef4552bffc25e17565b70ecfc0c680d89752361))

- **docs**: Rename test function
  ([`bbe7648`](https://github.com/russoz-ansible/andebox/commit/bbe7648e659344c463632bb799f1e3535227bf7e))

- **helper**: Use better names for attributes capturing stdout and stderr
  ([`3ec717e`](https://github.com/russoz-ansible/andebox/commit/3ec717e6cd550e17ed5a3765a98562c496057425))

- **yaml tests**: Make handling of pytest markers more generic
  ([`08526c4`](https://github.com/russoz-ansible/andebox/commit/08526c4f9dd3a80cf30087aff05e92b6d4b8ad7e))

- **yaml tests**: Simplify signature of load_test_cases()
  ([`2990f4d`](https://github.com/russoz-ansible/andebox/commit/2990f4da4053453a4ae6fc02ac90634387db8577))


## v1.1.1 (2025-06-02)

### Bug Fixes

- **action/yaml-doc**: Fix the processing of short description
  ([`cbbf95f`](https://github.com/russoz-ansible/andebox/commit/cbbf95f5bb85feaea00e1d14b458e14208a9dbcb))

- **action/yaml-doc**: Handle case when description is neither str nor list
  ([`c8fafab`](https://github.com/russoz-ansible/andebox/commit/c8fafab05614aaa94cab37ae23157ea8ddc60d9e))

### Chores

- **devcontainer**: Change the name of the devcontainer
  ([`566a0ce`](https://github.com/russoz-ansible/andebox/commit/566a0cee27984b7e6df6b2b963a44f6ef86ebc53))

### Code Style

- Move modeline comments to top of files
  ([`1dca1bb`](https://github.com/russoz-ansible/andebox/commit/1dca1bbf6fe7b6f47fe671e75a2c89c4ca6a7f5a))

### Testing

- **action/docsite**: Rename test and mark as xfail
  ([`1446614`](https://github.com/russoz-ansible/andebox/commit/144661457b71e86f8dfa2a7e4fe66626693dde32))

The test is passing, but it is quite long. A different strategy should be used for this one.

- **action/yaml-doc**: Add more testcases
  ([`05c4c8e`](https://github.com/russoz-ansible/andebox/commit/05c4c8e004c6d3a1270283e29774e55771736b42))


## v1.1.0 (2025-06-01)

### Bug Fixes

- **docsite**: Add missing dependency antsibull-docs
  ([`ea55648`](https://github.com/russoz-ansible/andebox/commit/ea5564827619a68d72ec9f6fd693661218b439f6))

### Chores

- Add documentation link to pyproject
  ([`45b50a8`](https://github.com/russoz-ansible/andebox/commit/45b50a8eeadfc88c44ff025acc44bc7b92f27727))

- Add no cover pragma to script entrypoint
  ([`692e7a2`](https://github.com/russoz-ansible/andebox/commit/692e7a240b1462538277530abc1094a332beb902))

- Add no cover pragma to script entrypoint (fix comment)
  ([`e7c5b23`](https://github.com/russoz-ansible/andebox/commit/e7c5b23f3816f1f8847ee5e281c3676669ba3368))

- Add no cover pragma to script entrypoint (fix comment)
  ([`d2cd4e1`](https://github.com/russoz-ansible/andebox/commit/d2cd4e16d3cd2f2de5868ed5f161506ac7f3bee9))

- Add no cover pragma to script entrypoint (slightly different)
  ([`4d810ac`](https://github.com/russoz-ansible/andebox/commit/4d810ac25e84ce3bc305529cd77616767acb65cd))

- Add no cover pragma to script entrypoint (with flake8 exclude)
  ([`0b6d9b5`](https://github.com/russoz-ansible/andebox/commit/0b6d9b519a54633124f3803e839abf2f1b535037))

- Add pragma on the function def line
  ([`91b469b`](https://github.com/russoz-ansible/andebox/commit/91b469b61ffeeb910e8ba2fa28e41eec185530e4))

- Ensure --cover=xml is passed to pytest
  ([`8594a1e`](https://github.com/russoz-ansible/andebox/commit/8594a1e8db76684e802c92d9464d3216e3fe32fb))

- Remove outdated comment from workflow
  ([`bfb54c3`](https://github.com/russoz-ansible/andebox/commit/bfb54c3794b437c6e5d0102bd0ddd916492839f9))

- **coverage**: Exclude code handling ImportError
  ([`790f161`](https://github.com/russoz-ansible/andebox/commit/790f161e806340ba33e2ab88a09d8db4d03ab21a))

- **deps**: Bump ruamel-yaml from 0.18.10 to 0.18.12
  ([`07b2e86`](https://github.com/russoz-ansible/andebox/commit/07b2e86c4c361c1be53cb0af46748321e6da20c8))

Bumps ruamel-yaml from 0.18.10 to 0.18.12.

--- updated-dependencies: - dependency-name: ruamel-yaml dependency-version: 0.18.12

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

### Continuous Integration

- Simplify pytest command line
  ([`ce9a295`](https://github.com/russoz-ansible/andebox/commit/ce9a29565ba6d197ec391c1284c76cd5d4d60c70))

- **dependabot**: Tuning parameters
  ([`e60e453`](https://github.com/russoz-ansible/andebox/commit/e60e4531094e308ec3c75213656554e95f424099))

- add devcontainers update - use auto rebase strategy for both updates - enable grouping for python
  updates

### Documentation

- **README**: Make file more concise
  ([`3a5a171`](https://github.com/russoz-ansible/andebox/commit/3a5a1716f3107b0a05afc771e0c982227fa5cc14))

- **todo**: Expand names of modules
  ([`ec66f10`](https://github.com/russoz-ansible/andebox/commit/ec66f1014fa2115f3e074fb9c6263bb266c41dde))

### Features

- **action/tox-test**: Update the initial tox config file
  ([`4241e41`](https://github.com/russoz-ansible/andebox/commit/4241e41f57800b3e07407be0e96fee3d53577d04))

Changes: * remove envs for Ansible community packages * update envs for `ansible-core` versions 2.15
  up to 2.18, plus `dev`

### Refactoring

- **action/ignores**: Simplify ResultLine with dataclass
  ([`39bcdaa`](https://github.com/russoz-ansible/andebox/commit/39bcdaac5defeba00bf48ec54dff8d05331b54c6))

- **action/ignores**: Use pathlib instead of os.path
  ([`251ff79`](https://github.com/russoz-ansible/andebox/commit/251ff79492b81e586cb6a1cd2ea570f370d67d31))

- **context**: Use pathlib instead of os.path
  ([`e918013`](https://github.com/russoz-ansible/andebox/commit/e9180134fc1f1ac7bb9002af28300d5fbce18b83))

### Testing

- Encapsulate AndeboxTestHelper creation in a fixture
  ([`7533fe9`](https://github.com/russoz-ansible/andebox/commit/7533fe9739672b31639b811fdb3236d087765b14))

- Improve execution of andebox in tests
  ([`913be97`](https://github.com/russoz-ansible/andebox/commit/913be973d64d0b83246e3546db1b376810da8931))

* `run_andebox` now mocks `cli:run()` * `AndeboxTestHelper` had to be adjusted to add the outcome of
  the executor to the `data` dict * executor for the `ansibletest` tests now ensure to add the
  return code (from `cli.run()`) in the test's data

- Make fixture git_repo suitable as setup for test helper
  ([`2778648`](https://github.com/russoz-ansible/andebox/commit/2778648db976ca14c5228ded3b3db3abad5d7d77))

- Revamp run_andebox fixture for test helper
  ([`65b8026`](https://github.com/russoz-ansible/andebox/commit/65b80264161b8b0f9f5fee9e6a317ac72848f3cc))

Now `run_andebox` can function straight in as `executor` in `AndeboxTestHelper`

- **action/docsite**: Add basic test
  ([`f683505`](https://github.com/russoz-ansible/andebox/commit/f68350546b0e66f8b4c17d5f6dd7a3ec10129b75))

- **action/runtime**: Add basic tests
  ([`63fca78`](https://github.com/russoz-ansible/andebox/commit/63fca785c36f6786963b30b0a082a1ed03c9644a))

- **coverage**: Move coverage config to .coveragerc
  ([`6fefd5a`](https://github.com/russoz-ansible/andebox/commit/6fefd5a532c70d55591545fe66555e6d41bef4ed))


## v1.0.0 (2025-05-31)

### Chores

- **deps-dev**: Bump pytest-mock from 3.14.0 to 3.14.1
  ([`a9dd3d1`](https://github.com/russoz-ansible/andebox/commit/a9dd3d1e932bc7948cdbe270d01c1d0cde2360d8))

Bumps [pytest-mock](https://github.com/pytest-dev/pytest-mock) from 3.14.0 to 3.14.1. - [Release
  notes](https://github.com/pytest-dev/pytest-mock/releases) -
  [Changelog](https://github.com/pytest-dev/pytest-mock/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest-mock/compare/v3.14.0...v3.14.1)

--- updated-dependencies: - dependency-name: pytest-mock dependency-version: 3.14.1

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump python-semantic-release from 9.21.1 to 10.0.2
  ([`2baa652`](https://github.com/russoz-ansible/andebox/commit/2baa65229f363703e269f72f89e2d85df7d74ca7))

Bumps [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
  from 9.21.1 to 10.0.2. - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v9.21.1...v10.0.2)

--- updated-dependencies: - dependency-name: python-semantic-release dependency-version: 10.0.2

dependency-type: direct:development

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>


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
