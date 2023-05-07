class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.num_nodes = 0

    class FibonacciNode:
        def __init__(self, key):
            self.key = key
            self.degree = 0
            self.marked = False
            self.parent = None
            self.child = None
            self.left = self
            self.right = self

        def addChild(self, child):
            if self.child:
                child.right = self.child.right
                child.left = self.child
                self.child.right.left = child
                self.child.right = child
            else:
                self.child = child
            child.parent = self
            self.degree += 1

        def removeChild(self, child):
            if child.right == child:
                self.child = None
            else:
                child.left.right = child.right
                child.right.left = child.left
            child.parent = None
            self.degree -= 1

    def insertNode(self, key):
        n = self.FibonacciNode(key)
        if self.min_node:
            n.right = self.min_node.right
            n.left = self.min_node
            self.min_node.right.left = n
            self.min_node.right = n
            if key < self.min_node.key:
                self.min_node = n
        else:
            self.min_node = n
        self.num_nodes += 1

    def union(self, heap2):
        self.mergeRootLists(heap2)
        if heap2.min_node:
            if not self.min_node or heap2.min_node.key < self.min_node.key:
                self.min_node = heap2.min_node
        self.num_nodes += heap2.num_nodes

    def mergeRootLists(self, heap2):
        if not self.min_node:
            self.min_node = heap2.min_node
            return

        if heap2 and heap2.min_node:
            self.min_node.right.left = heap2.min_node.left
            heap2.min_node.left.right = self.min_node.right
            self.min_node.right = heap2.min_node
            heap2.min_node.left = self.min_node


    def extractMin(self):
        if not self.min_node:
            return None
        min_node = self.min_node
        if min_node.right == min_node:
            self.min_node = None
        else:
            min_node.left.right = min_node.right
            min_node.right.left = min_node.left
            self.min_node = min_node.right

        child = min_node.child
        while child:
            child.parent = None
            child = child.right
        self.mergeRootLists(min_node.child)
        self.num_nodes -= 1
        return min_node.key

    def consolidate(self):
        max_degree = self.num_nodes.bit_length() + 1
        degree_table = [None] * max_degree
        roots = []

        current = self.min_node
        while True:
            degree = current.degree
            while degree_table[degree]:
                other = degree_table[degree]
                if other is current:
                    break
                current, other = self.mergeNodes(current, other)
                degree_table[degree] = None
                degree += 1
            degree_table[degree] = current
            roots.append(current)

            current = current.right
            if current == self.min_node:
                break
        self.min_node = None
        for node in roots:
            if not self.min_node or node.key < self.min_node.key:
                self.min_node = node

            self.min_node = None
            for node in degree_table:
                if node:
                    if not self.min_node or node.key < self.min_node.key:
                        self.min_node = node

    def decreaseKey(self, node, new_key):
        node.key = new_key
        parent = node.parent
        if parent and node.key < parent.key:
            self.cut(node, parent)
            self.cascadingCut(parent)
        if node.key < self.min_node.key:
            self.min_node = node

    def cut(self, node, parent):
        parent.removeChild(node)
        parent.degree -= 1
        node.parent = None
        node.marked = False

        node.right = self.min_node.right
        node.left = self.min_node
        self.min_node.right.left = node
        self.min_node.right = node

    def cascadingCut(self, node):
        parent = node.parent
        if parent:
            if not node.marked:
                node.marked = True
            else:
                self.cut(node, parent)
                self.cascadingCut(parent)

