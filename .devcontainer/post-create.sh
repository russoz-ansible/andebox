#!/usr/bin/env bash
# (C) 2026 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2026 Alexei Znamensky
# SPDX-License-Identifier: MIT

set -euo pipefail

pip install -U pip
pip install poetry pre-commit poethepoet

poetry install --no-interaction --with dev,docs
pre-commit install --install-hooks
mkdir -p ~/.ssh && chmod 700 ~/.ssh
