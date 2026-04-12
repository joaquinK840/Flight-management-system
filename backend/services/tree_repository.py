import json
import copy
from core.structures.avl_tree.tree import AVL
from core.structures.avl_tree.balance import update_height
from core.structures.bst_tree.bst import BST
from core.structures.node.node import Node
from core.structures.stack.stack import Stack
from services.serialize_tree import serialize_tree


class TreeRepository:
    """
    Patrón Repository: Encapsula la lógica del árbol y gestiona la pila de undo.
    Single Responsibility: Maneja operaciones CRUD sobre vuelos en el árbol.
    """

    def __init__(self, use_bst=False):
        """
        Inicializa el repositorio con un árbol (AVL o BST).
        
        Args:
            use_bst: Si True, usa BST; si False, usa AVL
        """
        self.tree = BST() if use_bst else AVL()
        self.use_bst = use_bst
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def _save_state(self):
        """
        Guarda el estado actual del árbol en la pila de undo.
        Serializa el árbol completo para poder restaurarlo después.
        """
        state = self._serialize_full_tree()
        self.undo_stack.push(state)
        # Limpiar redo_stack al tomar una nueva acción
        self.redo_stack.clear()

    def _serialize_full_tree(self):
        """
        Serializa el árbol completo para guardarlo en undo.
        
        Returns:
            Dict con toda la información del árbol
        """
        return {
            "root": self._serialize_node(self.tree.getRoot()),
            "rotation_counts": self.tree.rotation_counts.copy() if hasattr(self.tree, 'rotation_counts') else {},
            "mass_cancellation_count": self.tree.mass_cancellation_count if hasattr(self.tree, 'mass_cancellation_count') else 0,
            "stress_mode": self.tree.stress_mode if hasattr(self.tree, 'stress_mode') else False
        }

    def _serialize_node(self, node):
        """Serializa un nodo recursivamente para undo."""
        if node is None:
            return None
        return {
            "value": node.getValue(),
            "height": node.getHeight(),
            "datos": node.getDatos().copy() if node.getDatos() else None,
            "left": self._serialize_node(node.getLeftChild()),
            "right": self._serialize_node(node.getRightChild())
        }

    def _restore_tree_from_state(self, state):
        """
        Restaura un árbol desde un estado guardado.
        
        Args:
            state: Dict con estado del árbol
        """
        # Reconstruir árbol desde estado
        new_tree = BST() if self.use_bst else AVL()
        new_tree.root = self._deserialize_node(state["root"])
        if hasattr(new_tree, 'rotation_counts'):
            new_tree.rotation_counts = state.get("rotation_counts", {}).copy()
        if hasattr(new_tree, 'mass_cancellation_count'):
            new_tree.mass_cancellation_count = state.get("mass_cancellation_count", 0)
        if hasattr(new_tree, 'stress_mode'):
            new_tree.stress_mode = state.get("stress_mode", False)
        
        self.tree = new_tree

    def _deserialize_node(self, node_data):
        """Deserializa un nodo recursivamente."""
        if node_data is None:
            return None
        
        node = Node(node_data["value"], datos=node_data.get("datos"))
        node.setHeight(node_data.get("height", 1))
        
        left_child = self._deserialize_node(node_data.get("left"))
        right_child = self._deserialize_node(node_data.get("right"))
        
        if left_child:
            node.setLeftChild(left_child)
            left_child.setParent(node)
        
        if right_child:
            node.setRightChild(right_child)
            right_child.setParent(node)
        
        return node

    def insert_flight(self, flight_data: dict) -> dict:
        """
        Inserta un vuelo en el árbol.
        
        Args:
            flight_data: Dict con datos del vuelo (codigo, origen, etc.)
            
        Returns:
            Dict con árbol serializado y estado de operación
        """
        if "codigo" not in flight_data:
            raise ValueError("El vuelo debe tener 'codigo'")

        # Guardar estado anterior
        self._save_state()

        try:
            value = flight_data["codigo"]
            node = Node(value, datos=flight_data.copy())

            # Insertar según stress_mode
            if self.tree.stress_mode and not self.use_bst:
                # En stress_mode con AVL, insertar como BST (sin balanceo)
                self._insert_as_bst(node)
            else:
                # Insertar normalmente
                self.tree.insert(node)

            return {
                "status": "success",
                "message": f"Vuelo {value} insertado",
                "tree": self._get_serialized_tree()
            }
        except Exception as e:
            # Restaurar estado anterior en caso de error
            self.undo_stack.pop()
            raise e

    def _insert_as_bst(self, node):
        """Inserta un nodo como BST sin balanceo (para stress_mode)."""
        if self.tree.root is None:
            self.tree.root = node
        else:
            self._insert_bst_recursive(self.tree.root, node)
        # Actualizar alturas
        self._update_all_heights(self.tree.root)

    def _insert_bst_recursive(self, current, node):
        """Inserta recursivamente sin balanceo."""
        if node.getValue() == current.getValue():
            return
        
        if node.getValue() > current.getValue():
            if current.getRightChild() is None:
                current.setRightChild(node)
                node.setParent(current)
            else:
                self._insert_bst_recursive(current.getRightChild(), node)
        else:
            if current.getLeftChild() is None:
                current.setLeftChild(node)
                node.setParent(current)
            else:
                self._insert_bst_recursive(current.getLeftChild(), node)

    def _update_all_heights(self, node):
        """Actualiza alturas en todo el árbol."""
        if node is None:
            return
        self._update_all_heights(node.getLeftChild())
        self._update_all_heights(node.getRightChild())
        update_height(node)

    def delete_flight(self, codigo: int) -> dict:
        """
        Elimina un vuelo específico del árbol.
        Solo elimina el nodo, el sucesor reemplaza.
        
        Args:
            codigo: Código del vuelo a eliminar
            
        Returns:
            Dict con árbol serializado
        """
        if self.tree.getRoot() is None:
            raise ValueError(f"Vuelo {codigo} no encontrado")

        self._save_state()

        try:
            self.tree.delete(codigo)
            return {
                "status": "success",
                "message": f"Vuelo {codigo} eliminado",
                "tree": self._get_serialized_tree()
            }
        except Exception as e:
            self.undo_stack.pop()
            raise e

    def cancel_flight_subtree(self, codigo: int) -> dict:
        """
        Elimina un vuelo Y TODO SU SUBÁRBOL.
        Incrementa mass_cancellation_count.
        
        Args:
            codigo: Código del vuelo raíz del subárbol a cancelar
            
        Returns:
            Dict con árbol serializado
        """
        self._save_state()

        try:
            # Buscar el nodo
            node = self._find_node(self.tree.getRoot(), codigo)
            if node is None:
                raise ValueError(f"Vuelo {codigo} no encontrado")

            # Incrementar contador
            if hasattr(self.tree, 'mass_cancellation_count'):
                self.tree.mass_cancellation_count += 1

            # Obtener padre
            parent = node.getParent()

            # Desconectar subárbol eliminando la referencia del padre
            if parent is None:
                # Es la raíz: reemplazar por hijo derecho o izquierdo
                # Usando estrategia: si tiene hijo izquierdo, hacerlo raíz; si no, hijo derecho
                if node.getLeftChild() is not None:
                    self.tree.root = node.getLeftChild()
                    self.tree.root.setParent(None)
                elif node.getRightChild() is not None:
                    self.tree.root = node.getRightChild()
                    self.tree.root.setParent(None)
                else:
                    self.tree.root = None
            else:
                if parent.getLeftChild() == node:
                    parent.setLeftChild(None)
                else:
                    parent.setRightChild(None)

                # Recalcular heights desde el padre
                from core.structures.avl_tree.balance import check_balance
                if hasattr(self.tree, 'rotation_counts'):  # Es AVL
                    check_balance(self.tree, parent)

            return {
                "status": "success",
                "message": f"Vuelo {codigo} y subárbol cancelados",
                "tree": self._get_serialized_tree(),
                "mass_cancellations": self.tree.mass_cancellation_count if hasattr(self.tree, 'mass_cancellation_count') else 0
            }
        except Exception as e:
            self.undo_stack.pop()
            raise e

    def update_flight(self, codigo: int, updated_data: dict) -> dict:
        """
        Actualiza datos de un vuelo sin cambiar su posición en el árbol.
        
        Args:
            codigo: Código del vuelo
            updated_data: Dict con datos actualizados
            
        Returns:
            Dict con árbol serializado
        """
        self._save_state()

        try:
            node = self._find_node(self.tree.getRoot(), codigo)
            if node is None:
                raise ValueError(f"Vuelo {codigo} no encontrado")

            # Actualizar datos
            if node.getDatos() is None:
                node.setDatos({})
            
            current_datos = node.getDatos()
            current_datos.update(updated_data)
            node.setDatos(current_datos)

            return {
                "status": "success",
                "message": f"Vuelo {codigo} actualizado",
                "tree": self._get_serialized_tree()
            }
        except Exception as e:
            self.undo_stack.pop()
            raise e

    def undo(self) -> dict:
        """
        Restaura el estado anterior del árbol.
        
        Returns:
            Dict con árbol serializado del estado anterior
        """
        if self.undo_stack.is_empty():
            raise ValueError("No hay acciones para deshacer")

        # Guardar estado actual en redo
        self.redo_stack.push(self._serialize_full_tree())

        # Restaurar estado anterior
        previous_state = self.undo_stack.pop()
        self._restore_tree_from_state(previous_state)

        return {
            "status": "success",
            "message": "Operación deshecha",
            "tree": self._get_serialized_tree(),
            "undo_remaining": self.undo_stack.size()
        }

    def redo(self) -> dict:
        """
        Restaura el estado deshecho del árbol.
        
        Returns:
            Dict con árbol serializado del estado restaurado
        """
        if self.redo_stack.is_empty():
            raise ValueError("No hay acciones para rehacer")

        # Guardar estado actual en undo
        self.undo_stack.push(self._serialize_full_tree())

        # Restaurar estado de redo
        next_state = self.redo_stack.pop()
        self._restore_tree_from_state(next_state)

        return {
            "status": "success",
            "message": "Operación rehecha",
            "tree": self._get_serialized_tree()
        }

    def _find_node(self, node, codigo):
        """Busca un nodo por código recursivamente."""
        if node is None:
            return None
        
        if node.getValue() == codigo:
            return node
        elif codigo > node.getValue():
            return self._find_node(node.getRightChild(), codigo)
        else:
            return self._find_node(node.getLeftChild(), codigo)

    def _get_serialized_tree(self) -> dict:
        """Serializa el árbol actual para retornar en respuestas."""
        return serialize_tree(self.tree, depth=0, depth_limit=self.tree.depth_limit)

    def get_tree_metrics(self) -> dict:
        """Retorna métricas del árbol actual."""
        root = self.tree.getRoot()
        return {
            "height": root.getHeight() if root else 0,
            "leaves": self.tree.contar_hojas(),
            "total_nodes": self.tree.contar_nodos(),
            "rotation_counts": self.tree.rotation_counts.copy() if hasattr(self.tree, 'rotation_counts') else {},
            "total_rotations": sum(self.tree.rotation_counts.values()) if hasattr(self.tree, 'rotation_counts') else 0,
            "mass_cancellations": self.tree.mass_cancellation_count if hasattr(self.tree, 'mass_cancellation_count') else 0,
            "undo_states_available": self.undo_stack.size(),
            "tree_type": "BST" if self.use_bst else "AVL"
        }
