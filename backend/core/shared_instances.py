"""
Configuración global y singletons compartidos entre rutas.
"""

from core.structures.avl_tree.tree import AVL
from core.structures.bst_tree.bst import BST
from core.structures.queue.queue import Queue
from services.tree_repository import TreeRepository


avl = AVL()
bst = BST()
flight_queue = Queue()


class SharedTreeRepository(TreeRepository):
    """Repositorio que usa instancias compartidas de árboles."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.tree = avl
            cls._instance.use_bst = False
            # Inicializar pilas de undo/redo (no se inicializan en __init__ con __new__)
            from core.structures.stack.stack import Stack
            cls._instance.undo_stack = Stack()
            cls._instance.redo_stack = Stack()
        return cls._instance


flight_repository = SharedTreeRepository()
flight_repository = SharedTreeRepository()