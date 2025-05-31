# -*- coding: utf-8 -*-
# Copyright (c) 2021, Alexei Znamensky
# All rights reserved.
#
# This file is part of the Andebox project and is distributed under the terms
# of the BSD 3-Clause License. See LICENSE file for details.
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


# code: language=python tabSize=4
