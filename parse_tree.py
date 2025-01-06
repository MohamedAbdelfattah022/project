from __future__ import annotations
from typing import List

class ParseTreeNode:
    def __init__(self, name: str, children: List[ParseTreeNode] = None):
        self.name = name
        self.children = children if children else []

    def __str__(self, level=0):
        result = "  " * level + f"|-- {self.name}\n"
        for child in self.children:
            if isinstance(child, ParseTreeNode):
                result += child.__str__(level + 1)
        return result

    def add_child(self, child: ParseTreeNode):
        self.children.append(child)


