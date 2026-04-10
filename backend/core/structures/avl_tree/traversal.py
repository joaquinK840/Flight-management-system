# Funciones para recorridos del árbol AVL

def pre_order(node, result=None):
    """
    Recorrido preorden (raíz, izquierda, derecha).
    """
    if result is None:
        result = []
    if node is not None:
        result.append(node.getValue())
        pre_order(node.getLeftChild(), result)
        pre_order(node.getRightChild(), result)
    return result


def in_order(node, result=None):
    """
    Recorrido inorden (izquierda, raíz, derecha).
    """
    if result is None:
        result = []
    if node is not None:
        in_order(node.getLeftChild(), result)
        result.append(node.getValue())
        in_order(node.getRightChild(), result)
    return result


def post_order(node, result=None):
    """
    Recorrido postorden (izquierda, derecha, raíz).
    """
    if result is None:
        result = []
    if node is not None:
        post_order(node.getLeftChild(), result)
        post_order(node.getRightChild(), result)
        result.append(node.getValue())
    return result


def breadth_first_traversal(root):
    """
    Recorrido por niveles (anchura/BFS).
    Devuelve una lista de valores visitados en orden de nivel.
    """
    if root is None:
        return []
    
    resultado = []
    cola = [root]
    
    while cola:
        node = cola.pop(0)
        resultado.append(node.getValue())
        
        if node.getLeftChild():
            cola.append(node.getLeftChild())
        if node.getRightChild():
            cola.append(node.getRightChild())
    
    return resultado