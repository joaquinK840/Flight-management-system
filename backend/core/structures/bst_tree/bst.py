from core.structures.node.node import Node


class BST:
    """
    Binary Search Tree (sin balanceo automático).
    Utilizado para comparar contra AVL con los mismos datos.
    Single Responsibility: solo insertión ordenada, sin rotaciones.
    """

    def __init__(self):
        self.root = None

    def getRoot(self):
        return self.root

    def insert(self, node):
        """
        Inserta un nodo en el árbol manteniendo la propiedad BST.
        No aplica rotaciones (a diferencia de AVL).
        
        Args:
            node: Nodo con valor y posiblemente datos de vuelo
        """
        if self.root is None:
            self.root = node
        else:
            self._insert_recursive(self.root, node)

    def _insert_recursive(self, current, node):
        """
        Inserta recursivamente respetando la propiedad BST.
        """
        if node.getValue() == current.getValue():
            # Duplicado - no insertar
            return

        if node.getValue() > current.getValue():
            # Ir a la derecha
            if current.getRightChild() is None:
                current.setRightChild(node)
                node.setParent(current)
                self._update_height_branch(current)
            else:
                self._insert_recursive(current.getRightChild(), node)
        else:
            # Ir a la izquierda
            if current.getLeftChild() is None:
                current.setLeftChild(node)
                node.setParent(current)
                self._update_height_branch(current)
            else:
                self._insert_recursive(current.getLeftChild(), node)

    def _update_height_branch(self, node):
        """
        Actualiza alturas hacia la raíz (sin rotaciones).
        """
        while node is not None:
            left_height = node.getLeftChild().getHeight() if node.getLeftChild() is not None else 0
            right_height = node.getRightChild().getHeight() if node.getRightChild() is not None else 0
            node.setHeight(1 + max(left_height, right_height))
            node = node.getParent()

    def search(self, value):
        """
        Busca un nodo por valor en O(log n) promedio.
        """
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None:
            return None
        
        if value == node.getValue():
            return node
        elif value > node.getValue():
            return self._search_recursive(node.getRightChild(), value)
        else:
            return self._search_recursive(node.getLeftChild(), value)

    def contar_hojas(self):
        """Cuenta el número de hojas en el árbol."""
        return self._contar_hojas_recursivo(self.root)

    def _contar_hojas_recursivo(self, node):
        if node is None:
            return 0
        if node.getLeftChild() is None and node.getRightChild() is None:
            return 1
        return (
            self._contar_hojas_recursivo(node.getLeftChild()) +
            self._contar_hojas_recursivo(node.getRightChild())
        )

    def contar_nodos(self):
        """Cuenta el número total de nodos."""
        return self._contar_nodos_recursivo(self.root)

    def _contar_nodos_recursivo(self, node):
        if node is None:
            return 0
        return 1 + self._contar_nodos_recursivo(node.getLeftChild()) + self._contar_nodos_recursivo(node.getRightChild())

    def obtener_profundidad(self):
        """Obtiene la profundidad máxima del árbol."""
        return self._obtener_profundidad_recursiva(self.root) - 1

    def _obtener_profundidad_recursiva(self, node):
        if node is None:
            return 0
        return 1 + max(
            self._obtener_profundidad_recursiva(node.getLeftChild()),
            self._obtener_profundidad_recursiva(node.getRightChild())
        )
