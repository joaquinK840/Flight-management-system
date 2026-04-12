"""
Configuración global y singletons compartidos entre rutas.
Esto asegura que todas las rutas usen la misma instancia de árbol, cola, etc.
"""

from core.structures.avl_tree.tree import AVL
from core.structures.bst_tree.bst import BST
from core.structures.queue.queue import Queue
from services.tree_repository import TreeRepository


# =====================
# INSTANCIA COMPARTIDA DEL ÁRBOL AVL
# =====================
avl = AVL()


# =====================
# INSTANCIA COMPARTIDA DEL ÁRBOL BST
# =====================
bst = BST()


# =====================
# INSTANCIA COMPARTIDA DE COLA FIFO
# =====================
flight_queue = Queue()


# =====================
# REPOSITORIO COMPARTIDO (hereda de TreeRepository)
# =====================
class SharedTreeRepository(TreeRepository):
    """Repositorio que usa instancias compartidas de árboles."""
    
    _instance = None  # Singleton
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Inicializar con la instancia compartida de AVL
            cls._instance.tree = avl
            cls._instance.use_bst = False
        return cls._instance


# Crear única instancia del repositorio compartido
flight_repository = SharedTreeRepository()
flight_repository = SharedTreeRepository()

