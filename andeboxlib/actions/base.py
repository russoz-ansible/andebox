# -*- coding: utf-8 -*-
# (c) 2021, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from ..context import Context


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

    def run(self, context: Context) -> None:
        raise NotImplementedError()

    def __str__(self):
        return f"<AndeboxAction: {self.name}>"
