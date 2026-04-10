def _search_node(node, value):
    """
    Search for a node with the given value in the binary search tree.
    @param node: The current node in the tree.
    @param value: The value to search for.
    @return: The node with the specified value, or None if not found.
    """

    if node is None:
        return None

    if node.getValue() == value:
        return node

    if value > node.getValue():
        return _search_node(node.getRightChild(), value)

    return _search_node(node.getLeftChild(), value)
