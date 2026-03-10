class Node:

    def __init__(self, value):
        self.value = value
        self.parent = None
        self.leftChild = None
        self.rightChild = None

    def setRightChild(self, node):
        self.rightChild = node

    def getRightChild(self):
        return self.rightChild

    def setLeftChild(self, node):
        self.leftChild = node

    def getLeftChild(self):
        return self.leftChild

    def setParent(self, node):
        self.parent = node

    def getParent(self):
        return self.parent

    def getValue(self):
        return self.value