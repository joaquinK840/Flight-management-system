def rotate_right(tree, topNode):
    """Rotate right: left child becomes parent, top node moves to right subtree."""

    middleNode = topNode.getLeftChild()
    parent = topNode.getParent()

    rightChild = middleNode.getRightChild()

    middleNode.setRightChild(topNode)
    topNode.setParent(middleNode)

    if parent is None:

        tree.root = middleNode
        middleNode.setParent(None)

    else:

        if parent.getLeftChild() == topNode:
            parent.setLeftChild(middleNode)
        else:
            parent.setRightChild(middleNode)

        middleNode.setParent(parent)

    topNode.setLeftChild(rightChild)

    if rightChild is not None:
        rightChild.setParent(topNode)



def rotate_left(tree, topNode):
    """Rotate left: right child becomes parent, top node moves to left subtree."""

    middleNode = topNode.getRightChild()
    parent = topNode.getParent()

    leftChild = middleNode.getLeftChild()

    middleNode.setLeftChild(topNode)
    topNode.setParent(middleNode)

    if parent is None:

        tree.root = middleNode
        middleNode.setParent(None)

    else:

        if parent.getLeftChild() == topNode:
            parent.setLeftChild(middleNode)
        else:
            parent.setRightChild(middleNode)

        middleNode.setParent(parent)

    topNode.setRightChild(leftChild)

    if leftChild is not None:
        leftChild.setParent(topNode)