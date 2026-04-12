from .balance import check_balance
from .search import search_node

# Funciones para eliminación de nodos en el árbol AVL

# Método para identificar el caso de eliminación
# caso 1: nodo hoja
# caso 2: un solo hijo
# caso 3: dos hijos

def __identifyDeletionCase(node):
    if node.getLeftChild() is None and node.getRightChild() is None:
        return 1
    elif node.getLeftChild() is not None and node.getRightChild() is not None:
        return 3
    else:
        return 2

# Eliminar nodo hoja

def __deleteLeafNode(tree, node):
    parent = node.getParent()
    if parent is None:
        tree.root = None
    else:
        if parent.getLeftChild() == node:
            parent.setLeftChild(None)
        else:
            parent.setRightChild(None)
        node.setParent(None)
    check_balance(tree, parent)

# Eliminar nodo con un solo hijo

def __deleteNodeWithOneChild(tree, node):
    parent = node.getParent()
    child = node.getLeftChild() if node.getLeftChild() else node.getRightChild()
    if parent is None:
        tree.root = child
        child.setParent(None)
    else:
        if parent.getLeftChild() == node:
            parent.setLeftChild(child)
        else:
            parent.setRightChild(child)
        child.setParent(parent)
    node.setParent(None)
    check_balance(tree, parent)

# Eliminar nodo con dos hijos

def __deleteNodeWithTwoChildren(tree, node):
    # Buscar el sucesor (mínimo del subárbol derecho)
    successor = node.getRightChild()
    while successor.getLeftChild() is not None:
        successor = successor.getLeftChild()
    # Copiar valor y datos del sucesor al nodo a eliminar
    node.value = successor.getValue()
    node.setDatos(successor.getDatos())
    # Eliminar el sucesor (que tendrá a lo sumo un hijo derecho)
    if successor.getRightChild() is not None:
        __deleteNodeWithOneChild(tree, successor)
    else:
        __deleteLeafNode(tree, successor)

# Método principal de borrado

def __delete(tree, node):
    case = __identifyDeletionCase(node)
    if case == 1:
        __deleteLeafNode(tree, node)
    elif case == 2:
        __deleteNodeWithOneChild(tree, node)
    elif case == 3:
        __deleteNodeWithTwoChildren(tree, node)

# Interfaz pública para borrar por valor

def delete(tree, value):
    node = search_node(tree.root, value)
    if node is None:
        raise Exception(f"No se encontró el valor {value} en el árbol")
    __delete(tree, node)