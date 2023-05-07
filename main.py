import math

class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.num_nodes = 0

    class FibonacciNode:
        def __init__(self, key):
            self.key = key
            self.degree =0
            self.marked = False
            self.parent = None
            self.child = None
            self.left = self
            self.right = self
        def addChild(self,child):
            if self.child:
                child.right = self.child.right
                child.left = self.child
                self.child.right.left = self.child
                self.child.right = child
            else:
                self.child = child
            child.parent = self
            self.degree+=1
        def removeChild(self,child):
            if child.right == child:
                self.child=None
            else:
                child.left.right=child.right
                child.right.left=child.left

            child.parent = None
            self.degree-=1

    def insertNode(self,key):
        n=self.FibonacciNode(key)
        if self.min_node:
            n.right = self.min_node.right
            n.left = self.min_node
            self.min_node.right.left = n
            self.min_node.right = n
            if key<self.min_node.key:
                self.min_node = n
        else:
            self.min_node=n

        self.num_nodes+=1
    def getminNode(self):
        return self.min_node


heap=FibonacciHeap()
heap.insertNode(42);

