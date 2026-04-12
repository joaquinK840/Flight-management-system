def serialize_tree(tree, depth_limit=None):
    """
    Serialize AVL tree with optional depth-based penalties.
    
    Args:
        tree: AVL tree instance
        depth_limit: Critical depth limit for price penalties
        
    Returns:
        Serialized tree with price calculations based on depth
    """
    root = tree.getRoot()
    
    def __serialize_node(node, current_depth=0, depth_limit_val=None):
        if node is None:
            return None
        
        # Calculate price penalty if depth exceeds limit
        precio_final = node.getDatos().get('precioFinal', node.getDatos().get('precioBase', 0)) if node.getDatos() else node.getValue()
        
        # Apply penalty if node is deeper than critical limit
        if depth_limit_val is not None and current_depth > depth_limit_val:
            precio_base = node.getDatos().get('precioBase', 0) if node.getDatos() else 0
            penalty_factor = 1 + (0.05 * (current_depth - depth_limit_val))  # 5% per level beyond limit
            precio_final = int(precio_base * penalty_factor)
        
        node_data = node.getDatos() if node.getDatos() else {}
        
        return {
            "value": node.getValue(),
            "codigo": node.getValue(),
            "profundidad": current_depth,
            "nodoCritico": depth_limit_val is not None and current_depth > depth_limit_val,
            "precioFinal": precio_final,
            "datos": node_data,
            "left": __serialize_node(node.getLeftChild(), current_depth + 1, depth_limit_val),
            "right": __serialize_node(node.getRightChild(), current_depth + 1, depth_limit_val)
        }
    
    depth_limit_val = depth_limit if depth_limit is not None else (tree.depth_limit if hasattr(tree, 'depth_limit') else None)
    
    return {
        "root": __serialize_node(root, 0, depth_limit_val),
        "rotations": tree.rotation_counts if hasattr(tree, 'rotation_counts') else {}
    }
