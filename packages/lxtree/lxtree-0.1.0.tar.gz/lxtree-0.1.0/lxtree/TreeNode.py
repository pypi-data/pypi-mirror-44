# -*- coding: utf-8 -*-
from .TreeChars import TreeChars
from functools import reduce


class TreeNode(object):
    """
    Basic class to generate and print data trees.

    Attributes:
        name (str): Name of thee node
        children(lxtree.TreeNode list): Children of this node. By default `None`
    """

    def __init__(self, name='', children=None):
        self.name = name
        self.children = list(children) if children else []

    def __getitem__(self, i):
        return self.children[i]

    def __setitem__(self, i, value):
        self.children[i].children = value

    def __str__(self):
        return self.get_tree()

    def insert_child(self, node, index=0):
        """
        Insert the node into given position.

        Args:
            node (lxtree.TreeNode): Node to insert in the child list.
            index (int): Position where the child node will be inserted.
                By default `0`.

        Raises:
            TypeError: If `node` argument is not an instance of `lxtree.TreeNode`.

        Returns:
            lxtree.NodeTree: self
        """
        if not isinstance(node, TreeNode):
            raise TypeError('Children of a TreeNode must be also TreeNode objects')

        self._children.insert(index, node)

        return self

    def append_child(self, node):
        """
        Appends the node at the end of current children list.

        Args:
            node (lxtree.TreeNode): Node to append to children list.

        Raises:
            TypeError: If `node` argument is not an instance of `lxtree.TreeNode`.

        Returns:
            lxtree.NodeTree: self
        """
        if not isinstance(node, TreeNode):
            raise TypeError('Children of a TreeNode must be also TreeNode objects')

        self._children.append(node)

        return self

    def set_children(self, *new_children):
        """
        Set current node children list.

        Raises:
            TypeError: If any new child argument is not an instance of `lxtree.TreeNode`.

        Returns:
            lxtree.NodeTree: self
        """
        self.children = list(new_children)

        return self

    @property
    def children(self):
        """
        Children list of the node.

        Raises:
            TypeError: If children list is reassigned and any of it's content
                objects is not an instance of `lxtree.TreeNode`.
        """
        return self._children

    @children.setter
    def children(self, new_children):
        isTNode = lambda n: isinstance(n, TreeNode)
        allTrue = lambda a, b: a and b
        if len(new_children) > 0 and not reduce(allTrue, map(isTNode, new_children)):
            raise TypeError('Children of a TreeNode must be also TreeNode objects')

        self._children = new_children

    def _tree_lines(self):
        """
        Generate the tree and returns it in a string list,
            each item is a tree line.
        """
        lines = [self.name]
        for i, child in enumerate(self.children, start=1):
            child_lines = child._tree_lines()
            if i < len(self.children):
                lines.append(f'{TreeChars.VERT_RIGHT}{TreeChars.HORZ_LINE}{child_lines[0]}')
                treeChar = f'{TreeChars.VERT_LINE} '

            else:
                lines.append(f'{TreeChars.DOWN_RIGHT}{TreeChars.HORZ_LINE}{child_lines[0]}')
                treeChar = '  '

            for child_line in child_lines[1:]:
                lines.append(f'{treeChar}{child_line}')

        return lines

    def get_tree(self):
        """
        Generates a draw of the tree content.

        Returns:
            str: Tree figure.
        """
        return '\n'.join(self._tree_lines())

    @staticmethod
    def tree_from_dict(dict_data):
        """
        Creates a tree structure from a dictionary. Each key is a node, and values
            are a sub-dictionary with the childrens or `None` for leaf nodes.
            Example:
             `{'root': {'leaf1': {'leaf11': None, 'leaf12': None}, 'leaf2': None}}`

            Args:
                dict: Dict representing the tree structure.

            Returns:
                lxtree.TreeNode: Root of the tree.
                list of lxtree.TreeNode: List of nodes in case there are more
                    of one node at first leve depth.
        """
        result = []
        for key, value in dict_data.items():
            node = TreeNode(str(key))

            # If contains nodes call recursively
            if value:
                child_ren = TreeNode.tree_from_dict(value)

                # Method can return one or a many list
                if type(child_ren) == list:
                    node.children = child_ren

                else:
                    node.append_child(child_ren)

            result.append(node)

        if len(result) == 1:
            return result[0]

        return result
