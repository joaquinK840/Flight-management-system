from core.structures.node.node import Node


def _insert_node(node, new_node: Node):
    """
    Insert a new node into the binary search tree.
    @param node: The current node in the tree.
    @param new_node: The new node to be inserted.
    """

    if new_node.getValue() == node.getValue():
        print(f"Value {new_node.getValue()} already exists in the tree.")

    elif new_node.getValue() > node.getValue():

        if node.getRightChild() is None:

            node.setRightChild(new_node)
            new_node.setParent(node)

        else:

            _insert_node(node.getRightChild(), new_node)

    else:

        if node.getLeftChild() is None:

            node.setLeftChild(new_node)
            new_node.setParent(node)

        else:

            _insert_node(node.getLeftChild(), new_node)
