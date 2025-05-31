class Solution:

    def traverse_and_mark(self, root, dist):
        ans, tar, k = self.ans, self.tar, self.k
        if not root:
            return dist + 1
        if root == tar:
            dist = 0

        dist = min(dist, self.traverse_and_mark(root.left, dist + 1))
        prev_dist = dist
        dist = min(dist, self.traverse_and_mark(root.right, dist + 1))
        if prev_dist != dist:
            self.traverse_and_mark(root.left, dist + 1)
        if dist == k:
            ans.append(root.val)

        return dist + 1

    def distanceK(self, root, tar, k: int) -> list[int]:
        self.ans, self.tar, self.k = [], tar, k
        self.traverse_and_mark(root, dist=float('inf'))
        return self.ans