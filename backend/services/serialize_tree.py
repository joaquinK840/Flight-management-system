def _serialize_value(value):
    if hasattr(value, "to_dict") and callable(value.to_dict):
        return value.to_dict()
    return value


def _serialize_node(node, depth, depth_limit):
    if node is None:
        return None

    value = _serialize_value(node.getValue())
    if depth_limit is not None and depth >= depth_limit:
        return {
            "value": value,
            "left": None,
            "right": None,
        }

    return {
        "value": value,
        "left": _serialize_node(node.getLeftChild(), depth + 1, depth_limit),
        "right": _serialize_node(node.getRightChild(), depth + 1, depth_limit),
    }


def serialize_tree(tree, depth=0, depth_limit=None):
    root = tree.getRoot()
    if depth_limit is None and hasattr(tree, "depth_limit"):
        depth_limit = tree.depth_limit

    return {
        "root": _serialize_node(root, depth, depth_limit),
        "rotations": tree.get_rotation_by_type(),
    }