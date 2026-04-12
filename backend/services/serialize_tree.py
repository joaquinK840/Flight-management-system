def _serialize_value(value):
    if hasattr(value, "to_dict") and callable(value.to_dict):
        return value.to_dict()
    return value


def _apply_depth_metadata(data, depth, depth_limit):
    if not isinstance(data, dict):
        return data

    precio_base = float(data.get("precioBase", 0))
    penalizacion = float(data.get("penalizacion", 0))
    nodo_critico = depth_limit is not None and depth >= depth_limit

    if nodo_critico:
        data["nodoCritico"] = True
    else:
        data["nodoCritico"] = False
        penalizacion = 0.0

    data["penalizacion"] = penalizacion
    data["precioFinal"] = float(precio_base) + float(penalizacion)
    return data


def _serialize_node(node, depth, depth_limit):
    if node is None:
        return None

    datos = node.getDatos() if hasattr(node, "getDatos") else None
    value = _serialize_value(datos if datos is not None else node.getValue())
    value = _apply_depth_metadata(value, depth, depth_limit)
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

    rotations = None
    if hasattr(tree, "get_rotation_by_type"):
        rotations = tree.get_rotation_by_type()

    return {
        "root": _serialize_node(root, depth, depth_limit),
        "rotations": rotations,
    }