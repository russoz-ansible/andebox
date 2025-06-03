# -*- coding: utf-8 -*-
# code: language=python tabSize=4
# (C) 2021 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2021 Alexei Znamensky
# SPDX-License-Identifier: MIT
from ..context import ConcreteContext


class AndeboxAction:
    name = None
    help = None
    args = []  # of dict(names=[]: specs={})

    @classmethod
    def make_parser(cls, subparser):
        action_parser = subparser.add_parser(cls.name, help=cls.help)
        for arg in cls.args:
            action_parser.add_argument(*arg["names"], **arg["specs"])
        return action_parser

    def run(self, context: ConcreteContext) -> None:
        raise NotImplementedError()

    def __str__(self):
        return f"<AndeboxAction: {self.name}>"
