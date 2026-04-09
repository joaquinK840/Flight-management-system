def __serialize_node(node):
    if node is None:
        return None

    return {
        "value": node.getValue(),
        "left": __serialize_node(node.getLeftChild()),
        "right": __serialize_node(node.getRightChild())
    }

def serialize_tree(tree):
    root = tree.getRoot()

    return {
        "root": __serialize_node(root),
        "rotations": tree.get_rotation_by_type()
    }