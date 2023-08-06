from lxtree import TreeNode
from lxtree import TreeChars
from pathlib import Path
import unittest
import json


class TestTree(unittest.TestCase):

    _input_folder = Path(__file__).parent / 'input'
    _test_tree_view_filepath = _input_folder / 'test_tree_output.txt'
    _test_dict_tree_filepath = _input_folder / 'test_tree.json'

    def test_creation_and_child_addition(self):
        """
        Test TreeNode creation, `append_child`, `insert_child`, `set_children`
            and children setter.
        """
        test_tree = self._create_tree()

        # Test tree construction and 'getitem' method
        test_tree_error = 'Test tree is not as expected'
        self.assertEqual(test_tree.name, 'root-node', test_tree_error)
        self.assertEqual(test_tree.children[0].name, 'leaf1', test_tree_error)
        self.assertEqual(test_tree.children[0][0].name, 'sub-leaf11', test_tree_error)
        self.assertEqual(test_tree.children[0][1][0].name, 'sub-leaf121', test_tree_error)
        with self.assertRaises(IndexError):
            test_tree.children[1][0]

        # Child insertion
        test_tree.insert_child(TreeNode('leaf0'), 0)
        test_tree.children[1].insert_child(TreeNode('new-leaf12'), 1)
        self.assertEqual(test_tree.children[0].name, 'leaf0', 'Insertion failed')
        self.assertEqual(test_tree.children[1][1].name, 'new-leaf12', 'Insertion failed')

        # Child setter
        test_tree.children[1][2] = [TreeNode('new-leaf121'), TreeNode('new-leaf122')]
        self.assertEqual(test_tree[1][2][0].name, 'new-leaf121', 'Children list set failed')
        self.assertEqual(test_tree[1][2][1].name, 'new-leaf122', 'Children list set failed')

    def test_tree_str(self):
        """
        Test tree string representation.
        """
        # Load expected output
        expected_output = []
        with open(self._test_tree_view_filepath, 'r', encoding='utf-8') as f:
            for line in f:
                expected_output.append(line.rstrip())

        output = self._create_tree()._tree_lines()
        self._test_line_outputs(output, expected_output)

    def test_tree_from_dict(self):
        # Load tree dict from json
        with open(self._test_dict_tree_filepath, 'r') as f:
            tree_dict_data = json.load(f)

        test_tree = TreeNode.tree_from_dict(tree_dict_data)

        # Load expected_data
        expected_output = []
        with open(self._test_tree_view_filepath, 'r', encoding='utf-8') as f:
            for line in f:
                expected_output.append(line.rstrip())

        output = test_tree._tree_lines()
        self._test_line_outputs(output, expected_output)

    def _test_line_outputs(self, out_lines, expected_lines):
        """
        Check tree outputs.
        """
        self.assertEqual(len(out_lines), len(expected_lines), 'Line numbers does not match')
        for i in range(len(expected_lines)):
            self.assertEqual(expected_lines[i], out_lines[i], f'Line {i} does not match')

    def _create_tree(self):
        """
        Creates a basic tree. JSON representation:
            `{'root': {
                'leaf1': {
                    'sub-leaf11': None,
                    'sub-leaf12': {
                        'sub-leaf121': None
                    },
                    'sub-leaf13'
                },
                'leaf2': None
            }}`
        """
        root = TreeNode('root-node')
        root.append_child(TreeNode('leaf1').set_children(
                TreeNode('sub-leaf11'),
                TreeNode('sub-leaf12').append_child(TreeNode('sub-leaf121')),
                TreeNode('sub-leaf13')))
        root.append_child(TreeNode('leaf2'))

        return root
