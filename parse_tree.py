from __future__ import annotations
from typing import List

class ParseTreeNode:
    def __init__(self, name: str, children: List[ParseTreeNode] = None):
        self.name = name
        self.children = children if children else []
        print(f"Debug: Created ParseTreeNode with name: {self.name}")

    def __str__(self, level=0):
        result = "  " * level + f"|-- {self.name}\n"
        for child in self.children:
            if isinstance(child, ParseTreeNode):
                result += child.__str__(level + 1)
            else:
                print(f"Debug: Invalid child type in ParseTreeNode: {child}")
        return result

    def add_child(self, child: ParseTreeNode):
        if not isinstance(child, ParseTreeNode):
            raise TypeError(f"Expected ParseTreeNode, got {type(child)}")
        #print(f"Debug: Adding child to ParseTreeNode {self.name}: {child.name}")
        self.children.append(child)


