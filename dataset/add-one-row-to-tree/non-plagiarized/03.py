class Solution:
    def addOneRow(self, root, val: int, depth: int):
        if depth == 1:
            return TreeNode(val=val, left=root)

        queue = deque([(root, 1)])
        while queue:
            cur, cur_depth = queue.popleft()
            if cur_depth == depth - 1:
                left_subtree = cur.left
                right_subtree = cur.right
                cur.left = TreeNode(val, left=left_subtree)
                cur.right = TreeNode(val, right=right_subtree)
                continue

            if cur.left:
                queue.append((cur.left, cur_depth + 1))

            if cur.right:
                queue.append((cur.right, cur_depth + 1))

        return root
