class TreeNode():
    '''the definition of tree node'''

    def __init__(self, elem, left=None, right=None):
        self.ele = elem
        self.left = left
        self.right = right


class BinaryTree(object):
    '''initial function'''

    def __init__(self, root=None):
        # initial the root as None
        self.root = root
        self.stack = None
        self.it = None

    '''iter'''

    def __iter__(self):
        if self.root:
            self.it = 0
            if self.stack is None:
                self.stack = []
                queue = [self.root]
                self.stack.append(self.root)
                while queue:
                    currNode = queue.pop(0)
                    if currNode.left:
                        queue.append(currNode.left)
                        self.stack.append(currNode.left)
                    if currNode.right:
                        queue.append(currNode.right)
                        self.stack.append(currNode.right)
        return self.it

    '''next'''

    def __next__(self):
        if (self.it >= len(self.stack)) or (self.it is None):
            raise StopIteration
        else:
            self.it += 1
            return self.it

    '''find the node which its elem equal to the item '''

    def findElem(self, item):
        parentNode = None
        currNode = None
        if self.root is None:
            print("the set is empty")
            res = False
        else:
            queue = [self.root]
            while queue:
                currNode = queue.pop(0)
                if currNode.ele == item:
                    res = True
                    # if item is equal to the root.ele, return node
                    break
                elif currNode.ele > item:
                    if currNode.left is not None:
                        parentNode = currNode
                        # search the left child tree
                        queue.append(currNode.left)
                    else:                 # the item is not in the set
                        currNode = None
                        parentNode = None
                        res = False
                        break
                else:
                    if currNode.right is not None:
                        parentNode = currNode
                        # search the right child tree
                        queue.append(currNode.right)
                    else:
                        parentNode = None
                        currNode = None
                        res = False
                        break
        return res, parentNode, currNode

    def add(self, item):
        '''add node to tree'''
        node = TreeNode(item)           # instance of the node
        if(self.root is None):          # if the set is empty
            self.root = node
            return True
        else:
            queue = [self.root]
            while queue:
                currNode = queue.pop(0)
                if currNode.ele == item:  # if the item is already in the set
                    print("the item is already in the set")
                    return False
                elif currNode.ele > item:
                    if currNode.left:
                        # if the item is smaller than the currNode.ele
                        queue.append(currNode.left)
                    else:
                        currNode.left = node
                        return True
                else:          # if the item is larger than the currNode.ele
                    if currNode.right:
                        queue.append(currNode.right)
                    else:
                        currNode.right = node
                        return True

    '''delete the item'''

    def delete(self, item):
        # search the item wheather in the set
        res, parentNode, currNode = self.findElem(item)
        if not res:
            # if item does not in the set, return false
            return False
        else:
            if currNode.left:
                parentOfInsteadNode = currNode
                insteadNode = currNode.left
                if insteadNode.right:
                    while insteadNode.right:
                        parentOfInsteadNode = insteadNode
                        insteadNode = insteadNode.right
                    parentOfInsteadNode.right = insteadNode.left
                    insteadNode.left = currNode.left
                insteadNode.right = currNode.right
                currNode.left = None
                currNode.right = None
            elif currNode.right:
                parentOfInsteadNode = currNode
                insteadNode = currNode.right
                if insteadNode.left:
                    while insteadNode.left:
                        parentOfInsteadNode = insteadNode
                        insteadNode = insteadNode.left
                    parentOfInsteadNode.left = insteadNode.right
                    insteadNode.right = currNode.right
                currNode.right = None
            else:
                parentOfInsteadNode = None
                insteadNode = None
            if parentNode:
                if parentNode.left == currNode:
                    parentNode.left = insteadNode
                else:
                    parentNode.right = insteadNode
            else:
                self.root = insteadNode
            return True

    '''size'''

    def getSize(self):
        if self.root is None:
            return 0        # if the set is empty, return 0
        else:               # count the size
            size = 0
            # queue for count
            queue = [self.root]
            while queue:
                currNode = queue.pop(0)
                size += 1
                if currNode.left:
                    queue.append(currNode.left)
                if currNode.right:
                    queue.append(currNode.right)
            return size

    '''to list'''

    def to_list(self):
        res = []
        self.__iter__()
        if self.it is None:
            return res
        else:
            while self.it < len(self.stack):
                node = self.stack[self.it]
                res.append(node.ele)
                self.__next__()
        return res

    '''from list'''

    def from_list(self, tlist):
        if tlist == []:
            return
        else:
            for i in tlist:
                self.add(i)
        return

    '''filter, the rule is defined by func'''

    def filter(self, func):
        self.it = self.__iter__()
        if self.it is None:
            return
        else:
            de_stack = []
            while self.it < len(self.stack):
                value = self.stack[self.it].ele
                if func(value) is False:
                    de_stack.append(self.stack[self.it])
                    self.stack.pop(self.it)
                self.__next__()
            for item in de_stack:
                # self.stack.remove(item)
                self.delete(item.ele)
            return

    '''map, the rule is defined by func'''

    def map(self, func):
        self.it = self.__iter__()
        if self.it is None:
            return
        else:
            while self.it < len(self.stack):
                currNode = self.stack[self.it]
                currNode.ele = func(currNode.ele)
                self.__next__()
            return

    '''reduce'''

    def reduce(self, func):
        it = self.__iter__()
        value = 0
        while it < len(self.stack):
            value += func(self.stack[self.it].ele)
            it = self.__next__()
        return value

    '''mempty'''

    def mempty(self):
        return BinaryTree()

    '''mconcat'''

    def mconcat(self, tree):
        BT = BinaryTree()
        if self.root and tree.root:
            it1 = self.__iter__()
            it2 = tree.__iter__()
            while it1 < len(self.stack):
                BT.add(self.stack[it1].ele)
                it1 = self.__next__()
            while it2 < len(tree.stack):
                BT.add(tree.stack[it2].ele)
                it2 = tree.__next__()
            return BT
        elif self.root is None and tree.root:
            return tree
        elif tree.root is None and self.root:
            return self
        else:
            return BT
