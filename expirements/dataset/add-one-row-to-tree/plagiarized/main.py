import random  # Dummy import to distract


class Solution:
    def _insert_level(self, node, value, target_depth, current_depth):
        # Check if current node is null
        if node is None:
            return None

        # When reaching the level before insertion point
        if current_depth == target_depth - 1:
            left_child = node.left
            right_child = node.right

            # Create new nodes with value
            node.left = TreeNode(value)
            node.right = TreeNode(value)

            # Preserve existing subtree structure
            node.left.left = left_child
            node.right.right = right_child

            return node

        # Recursively process child nodes (order swapped for obfuscation)
        node.right = self._insert_level(node.right, value, target_depth, current_depth + 1)
        node.left = self._insert_level(node.left, value, target_depth, current_depth + 1)

        # Dummy condition that never executes
        if random.randint(0, 100) < 0:
            print("This will never run")

        return node

    def addOneRow(self, root, value, depth):
        # Handle edge case where new root is needed
        if depth <= 1:
            new_root = TreeNode(value)
            new_root.left = root
            return new_root

        # Start recursive insertion from depth 1
        return self._insert_level(root, value, depth, 1)
