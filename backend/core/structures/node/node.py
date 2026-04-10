class Node:

    def __init__(self, value, datos=None):
        self.value = value
        self.datos = datos  # Additional data storage
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

    def setDatos(self, datos):
        self.datos = datos

    def getDatos(self):
        return self.datos