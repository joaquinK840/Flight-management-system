from .balance import check_balance
from .search import search_node


def __cancel(tree, node):
    parent = node.getParent()

    if parent is not None:

        if parent.getLeftChild() == node:
            parent.setLeftChild(None)
        else:
            parent.setRightChild(None)

        check_balance(tree, parent)

    else:
        tree.root = None

def cancel(tree, value):
    node = search_node(tree.root, value)
    if node is None:
        raise Exception(f"No se encontró el valor {value} en el árbol")
    __cancel(tree, node)