# code: language=python tabSize=4
# (C) 2026 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2026 Alexei Znamensky
# SPDX-License-Identifier: MIT
#
# Internal noxfile used by andebox's nox-test action.
# Not intended to be used directly by end users.
import nox

from andebox.actions.noxtest import register_sessions

register_sessions(nox)
