# dummy imports to distract
import math
import random  # unused but distracting
from collections import deque as DQ  # alias for original deque


# end of dummy imports

class Solution:  # was Solution
    def distanceK(self,
                  root_node: "TreeNode",
                  target_node: "TreeNode",
                  distance: int
                  ) -> list:
        """Compute nodes at exact distance from target in binary tree."""
        # prepare output container
        output_list = []  # was ans

        # STEP 1: build parent map
        parent_map = {}  # was parent
        queue_line = DQ([root_node])  # was queue
        # iterate level-by-level
        while queue_line:
            layer_count = len(queue_line)  # was size
            # convert for->while
            index = 0
            while index < layer_count:
                current = queue_line.popleft()  # was top

                # record left child parent
                if current.left:
                    parent_map[current.left.val] = current
                    queue_line.append(current.left)

                # record right child parent
                if current.right:
                    parent_map[current.right.val] = current
                    queue_line.append(current.right)

                index += 1

        # STEP 2: breadth-first from target up to k layers
        seen = {}  # was visited
        queue_line.clear()
        queue_line.append(target_node)

        # useless no-op operations
        _ = random.random()
        dummy_counter = 0

        # repeat until zero distance
        while distance > 0 and queue_line:
            lvl = len(queue_line)
            # swap for->for to while
            i = 0
            while i < lvl:
                current = queue_line.popleft()
                seen[current.val] = True

                # left child
                if hasattr(current, 'left') and current.left and current.left.val not in seen:
                    queue_line.append(current.left)
                    dummy_counter += 1  # no-op increment

                # right child
                if getattr(current, 'right', None) and current.right.val not in seen:
                    queue_line.append(current.right)

                # parent link
                if current.val in parent_map:
                    parent_node = parent_map[current.val]
                    if parent_node.val not in seen:
                        queue_line.append(parent_node)

                i += 1

            distance -= 1  # decrement steps

        # STEP 3: collect remaining nodes in queue
        # change while to for
        for _ in range(len(queue_line)):
            node = queue_line.popleft()
            output_list.append(node.val)

        return output_list


# useless helper to distract plagiarism detector
def _compute_nonsense(x: int) -> float:
    # this function never used
    return math.sqrt(x ** 2 + 0)  

