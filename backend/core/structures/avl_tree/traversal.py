from collections import deque

# Funciones para recorridos del árbol AVL

def in_order(node):
    """In-order traversal (left, root, right)."""
    result = []
    
    def _in_order(n):
        if n is None:
            return
        _in_order(n.getLeftChild())
        result.append(n.getValue())
        _in_order(n.getRightChild())
    
    _in_order(node)
    return result


def breadth_first_traversal(node):
    """Breadth-first traversal (BFS) level by level."""
    if node is None:
        return []
    
    result = []
    queue = deque([node])
    
    while queue:
        current = queue.popleft()
        result.append(current.getValue())
        
        if current.getLeftChild() is not None:
            queue.append(current.getLeftChild())
        if current.getRightChild() is not None:
            queue.append(current.getRightChild())
    
    return result


def pre_order(node):
    """Pre-order traversal (root, left, right)."""
    result = []
    
    def _pre_order(n):
        if n is None:
            return
        result.append(n.getValue())
        _pre_order(n.getLeftChild())
        _pre_order(n.getRightChild())
    
    _pre_order(node)
    return result


def post_order(node):
    """Post-order traversal (left, right, root)."""
    result = []
    
    def _post_order(n):
        if n is None:
            return
        _post_order(n.getLeftChild())
        _post_order(n.getRightChild())
        result.append(n.getValue())
    
    _post_order(node)
    return result