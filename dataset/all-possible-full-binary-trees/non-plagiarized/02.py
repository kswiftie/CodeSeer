class Solution:
    def allPossibleFBT(self, n: int):
        return (f:=cache(lambda n:(n==1)*[TreeNode()]+[TreeNode(0,l,r) for k in range(1,n-1,2) for l in f(k) for r in f(n-1-k)]))(n)