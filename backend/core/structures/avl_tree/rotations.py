"""
AVL tree rotation operations.

This module provides the fundamental rotation operations used to maintain
AVL tree balance: left rotations and right rotations.
"""


def rotate_right(tree, topNode):
    """
    Perform a right rotation on the given node.

    In a right rotation, the left child becomes the new parent,
    and the original node becomes the right child of its former left child.

    Args:
        tree (AVL): The AVL tree instance
        topNode (Node): The node to rotate (becomes right child)
    """
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
    """
    Perform a left rotation on the given node.

    In a left rotation, the right child becomes the new parent,
    and the original node becomes the left child of its former right child.

    Args:
        tree (AVL): The AVL tree instance
        topNode (Node): The node to rotate (becomes left child)
    """
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