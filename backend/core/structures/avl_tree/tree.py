from core.structures.node.node import Node
from core.structures.stack.stack import Stack

from .balance import check_balance, get_balance_factor, get_height
from .delete import delete
from .insert import insert_node
from .search import search_node
from .traversal import breadth_first_traversal, in_order, post_order, pre_order


class AVL:
    """
    AVL Tree implementation for storing and managing data with self-balancing properties.

    Attributes:
        root (Node): The root node of the AVL tree.
        undo_stack (Stack): Stack for undo operations.
        redo_stack (Stack): Stack for redo operations.
    """

    def __init__(self):
        self.root = None
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def getRoot(self):
        return self.root

    def altura(self, nodo):
        """
        Returns the height of a node.
        """
        return get_height(nodo)

    def obtenerFactorBalance(self, nodo):
        """
        Calculates and returns the balance factor of a node.
        """
        return get_balance_factor(nodo)

    def insert(self, node):
        """
        Insert a node into the AVL tree with undo support.
        """
        # Save current state for undo
        self._save_state()

        if self.root is None:
            self.root = node
        else:
            insert_node(self, self.root, node)

    def insertar(self, clave, datos):
        """
        Insert a new node with key and data.
        """
        nuevo_nodo = Node(clave)
        nuevo_nodo.setDatos(datos)
        self.insert(nuevo_nodo)

    def search(self, value):
        """
        Search for a node with the given value.
        """
        if self.root is None:
            raise Exception("El árbol no tiene raíz")
        return search_node(self.root, value)

    def delete(self, value):
        """
        Delete a node with the given value with undo support.
        """
        # Save current state for undo
        self._save_state()

        delete(self, value)

    def eliminar(self, clave):
        """
        Delete a node with the specified key.
        """
        self.delete(clave)

    def cancelar_vuelo(self, clave):
        """
        Cancel flight: delete node and all its descendants.
        """
        # Save current state for undo
        self._save_state()

        node = self.search(clave)
        if node is not None:
            self._delete_subtree(node)

    def _delete_subtree(self, node):
        """
        Delete a node and all its descendants.
        """
        if node is None:
            return

        # Delete left subtree
        if node.getLeftChild():
            self._delete_subtree(node.getLeftChild())

        # Delete right subtree
        if node.getRightChild():
            self._delete_subtree(node.getRightChild())

        # Remove this node from its parent
        parent = node.getParent()
        if parent is not None:
            if parent.getLeftChild() == node:
                parent.setLeftChild(None)
            else:
                parent.setRightChild(None)
        else:
            # This is the root
            self.root = None

    def undo(self):
        """
        Undo the last operation.
        """
        if not self.undo_stack.is_empty():
            # Save current state for redo
            self.redo_stack.push(self._get_current_state())

            # Restore previous state
            previous_state = self.undo_stack.pop()
            self._restore_state(previous_state)
            return True
        return False

    def redo(self):
        """
        Redo the last undone operation.
        """
        if not self.redo_stack.is_empty():
            # Save current state for undo
            self._save_state()

            # Restore next state
            next_state = self.redo_stack.pop()
            self._restore_state(next_state)
            return True
        return False

    def _save_state(self):
        """
        Save the current tree state to undo stack.
        """
        state = self._serialize_tree()
        self.undo_stack.push(state)
        # Clear redo stack when new action is performed
        self.redo_stack.clear()

    def _get_current_state(self):
        """
        Get the current tree state.
        """
        return self._serialize_tree()

    def _serialize_tree(self):
        """
        Serialize the current tree structure.
        """
        def serialize_node(node):
            if node is None:
                return None
            return {
                'value': node.getValue(),
                'data': node.getDatos(),
                'left': serialize_node(node.getLeftChild()),
                'right': serialize_node(node.getRightChild())
            }
        return serialize_node(self.root)

    def _restore_state(self, state):
        """
        Restore tree from serialized state.
        """
        def deserialize_node(data):
            if data is None:
                return None
            node = Node(data['value'])
            node.setDatos(data['data'])
            node.setLeftChild(deserialize_node(data['left']))
            node.setRightChild(deserialize_node(data['right']))

            # Set parent references
            if node.getLeftChild():
                node.getLeftChild().setParent(node)
            if node.getRightChild():
                node.getRightChild().setParent(node)

            return node

        self.root = deserialize_node(state)

    def contar_hojas(self):
        """
        Count the number of leaf nodes in the tree.
        """
        return self._contar_hojas_recursivo(self.root)

    def _contar_hojas_recursivo(self, nodo):
        """
        Recursive helper to count leaves.
        """
        if nodo is None:
            return 0

        if nodo.getLeftChild() is None and nodo.getRightChild() is None:
            return 1

        return (self._contar_hojas_recursivo(nodo.getLeftChild()) +
                self._contar_hojas_recursivo(nodo.getRightChild()))

    def get_profundidad(self):
        """
        Get the depth (height) of the tree.
        """
        return self.altura(self.root)

    def get_raiz_valor(self):
        """
        Get the root value.
        """
        return self.root.getValue() if self.root else None

    def preOrden(self):
        """
        Returns the nodes of the tree in pre-order traversal (root, left, right).
        """
        return pre_order(self.root)

    def inOrden(self):
        """
        Returns the nodes of the tree in in-order traversal (left, root, right).
        """
        return in_order(self.root)

    def postOrden(self):
        """
        Returns the nodes of the tree in post-order traversal (left, right, root).
        """
        return post_order(self.root)

    def recorridoAnchura(self):
        """
        Performs a breadth-first traversal (BFS) of the AVL tree
        and returns a list of visited node values.
        """
        return breadth_first_traversal(self.root)

    def consultarDistancia(self, x_min, x_max, y_min, y_max):
        """
        Returns a list of node data whose 'x' and 'y' values
        are within the specified range.
        """
        resultado = []
        self._consultarDistancia(self.root, x_min, x_max, y_min, y_max, resultado)
        return resultado

    def _consultarDistancia(self, nodo, x_min, x_max, y_min, y_max, resultado):
        """
        Recursive helper function for range query on coordinates.
        """
        if nodo is None:
            return

        # Get the node's data
        datos = nodo.getValue() if hasattr(nodo, 'datos') else nodo.getValue()

        # Check if datos is a dictionary with x and y keys
        if isinstance(datos, dict):
            x = datos.get('x') or datos.get('x0') or datos.get('world_x')
            y = datos.get('y') or datos.get('y0') or datos.get('world_y')

            if x is not None and y is not None:
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    resultado.append(datos)

        # Recursively search left and right subtrees
        self._consultarDistancia(nodo.getLeftChild(), x_min, x_max, y_min, y_max, resultado)
        self._consultarDistancia(nodo.getRightChild(), x_min, x_max, y_min, y_max, resultado)

    def mostrarArbol(self, nodo=None, nivel=0, lado="Raíz"):
        """
        Recursively prints the structure of the tree for visualization and debugging.
        """
        if nodo is None:
            nodo = self.root

        if nodo is None:
            print("El árbol está vacío")
            return

        # Print current node
        indent = "  " * nivel
        valor = nodo.getValue()
        bf = self.obtenerFactorBalance(nodo)
        altura = self.altura(nodo)
        print(f"{indent}[{lado}] Valor: {valor}, Altura: {altura}, Balance: {bf}")

        # Print left subtree
        if nodo.getLeftChild():
            self.mostrarArbol(nodo.getLeftChild(), nivel + 1, "Izq")

        # Print right subtree
        if nodo.getRightChild():
            self.mostrarArbol(nodo.getRightChild(), nivel + 1, "Der")